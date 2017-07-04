#!/usr/bin/env python
#-*- coding: utf-8-*-


from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import auth
from ..main.forms import LoginForm, RegisterForm
from ..models import User
from .. import db
from ..email import send_email
from flask_login import current_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	print('into login..............{}'.format(form.email.data))
	# 验证是否收到表单函数
	if form.validate_on_submit():
		print('into validate_on_submit..............{}'.format(form.email.data))
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			# 标记用户已登录，之后该用户可以通过login_required
			# login_user()函数还有一个可选可选的“记住我”布尔值
			login_user(user, form.remember_me.data)
			print('next:{}'.format(request.args.get('next')))
			return redirect(request.args.get('next') or url_for('main.home'))
		# 模板通过Flask的get_flashed_ messages()函数去调用flash的消息
		# 注：get_flashed_messages()函数获取的消息在下次调用时不会再次返回
		flash(' invalid username or password.')
	# Flask 提供的 render_template 函数把 Jinja2 模板引擎集成到了程序中
	# render_template 函数的第一个参数是模板的文件名。随后的参数都是键值对，表示模板中变量对应的真实值。
	return render_template('auth/login.html', form=form)


@auth.route('/logout')
#login_required 只有登录了的用户才能通过（login_user(user, form.remember_me.data)）
@login_required
def logout():
	#删除并重设用户会话，和login_user对应
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.home'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegisterForm()
	#print('into register..............{}'.format(form.email.data))
	if form.validate_on_submit():
		user = User(email=form.email.data,
					username=form.username.data,
					password=form.password.data
					)
		#print('into validate_on_submit..............{}'.format(form.email.data))
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		send_email('zhougang@kiyozawa.com', 'Confirm Your Accout',
					'auth/email/confirm', user=user, token=token)
		flash('A confirmation email has been sent to you by email.')
		return redirect(url_for('main.home'))
	return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	print('into confirm..............')
	print('current_user.confirmed...............{}'.format(current_user.confirmed))
	print('current_user.username...............{}'.format(current_user.username))
	#print('current_user.confirm...............{}'.format(current_user.confirm(token)))
	print('is_authenticated...............{}'.format(current_user.is_authenticated))
	if current_user.confirmed:
		return redirect(url_for('main.home'))
	if current_user.confirm(token):
		flash('You have confirmed your account. Thanks!')
	else:
		flash('The confirmation link is invalid or expired.')
	return redirect(url_for('main.home'))


# 处理程序中过滤未确认的账户 
@auth.before_app_request
def before_request():
	print('into before_request...............')
	print('is_authenticated...............{}'.format(current_user.is_authenticated))
	#print('request.endpoint[:5]...............{}'.format(request.endpoint[:5]))
	print('request................{}'.format(request))
	# 1.用户已登录（current_user.is_authenticated() 必须返回 True）
	# 2.用户的账户还未确认
	# 3.请求的端点（使用 request.endpoint 获取）不在认证蓝本中
	# 满足以上 3 个条件，则会被重定向到 /auth/unconfirmed 路由
	if current_user.is_authenticated:
		current_user.ping()
		if not current_user.confirmed and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
			return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
	print('into unconfirmed...............{}'.format(current_user.is_anonymous))
	print('is_authenticated...............{}'.format(current_user.is_authenticated))
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.home'))
	return render_template('auth/unconfirmed.html')


# 重新发送账户确认邮件 
@auth.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_email('zhougang@kiyozawa.com', 'Confirm Your Accout',
					'auth/email/confirm', user=current_user, token=token)
	flash('A new confirmation email has been sent to you by email.')
	return redirect(url_for('main.home'))



