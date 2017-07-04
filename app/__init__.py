#!/usr/bin/env python
#-*- coding: utf-8-*-


from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config 
from flask_login import LoginManager
from flask_pagedown import PageDown


bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
pagedown = PageDown()


# 程序的工厂函数，接受一个参数，是程序使用的配置名
# 作用： 是延迟创建程序实例
def create_app(config_name):
	# Flask构造函数需要指定一个参数，即程序主模块或者包的名字。变量__name__指的是模块明
	# Flask用这个参数决定程序的根目录，以便稍后查找根目录的资源文件
	app = Flask(__name__)
	# from_object() 方法直接将配置类导入程序
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	bootstrap.init_app(app)
	mail.init_app(app)
	# 本地化日期和时间初始化
	moment.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	pagedown.init_app(app)
	#import pdb
	#pdb.set_trace()
	if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
		from flask_sslify import SSLify
		#sslify = SSLify(app)
	
	# 注册蓝本	
	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix='/auth')

	from .api_1_0 import api as api_1_0_blueprint
	app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

	return app
