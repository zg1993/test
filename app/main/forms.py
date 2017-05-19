#!/usr/bin/env python
#-*- coding: utf-8-*-

#from FlaskForm import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField, TextAreaField, SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from ..models import User, Role
from wtforms import ValidationError
from flask_pagedown.fields import PageDownField 


class NameForm(FlaskForm):
	name = StringField('name:', validators = [Required()])
	submit = SubmitField('submit')


class LoginForm(FlaskForm):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	password = PasswordField('Password', validators=[Required()])
	remember_me = BooleanField('Keep me log in')
	submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
	email = StringField('Email', validators=[Required(), Length(1, 64), Email()])
	username = StringField('username', validators=[
		Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'invalid format')])
	password = PasswordField('password', validators=[
		Required(), EqualTo('password2', message='Password must match.')])
	password2 = PasswordField('Confirm password', validators=[Required()])
	submit = SubmitField('Register')


	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')


#edit user info
class EditProfileForm(FlaskForm):
	name = StringField('Real name', validators=[Length(0, 64)])
	location = StringField('Location', validators=[Length(0, 64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')


class EditProfileAdminForm(FlaskForm):
	email = StringField('Email', validators=[Required(),Length(1, 46), 
											Email()])
	username = StringField('Username', validators=[
		Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_]*$', 0, 'invalid format')])
	confirmed = BooleanField('Confirmed')
	role = SelectField('Role', coerce=int)
	name = StringField('Real name', validators=[Length(0, 64)])
	location = StringField('Location', validators=[Length(0, 64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')


	def __init__(self, user, *args, **kwargs):
		super(EditProfileAdminForm, self).__init__(*args, **kwargs)
		self.role.choices = [(role.id, role.name) for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_email(self, field):
		if field.data != self.user.email and User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self, field):
		if field.data != self.user.username and User.query.filter_by(username=field.data).first():
			raise ValidationError('Email already registered.')


#add aricle form
class PostForm(FlaskForm):
	#body = TextAreaField('what\'s on your mind?', validators=[Required()])
	body = PageDownField('what\'s on your mind?', validators=[Required()])
	submit = SubmitField('Submit')


#add comment form
class CommentForm(FlaskForm):
	body = StringField('', validators=[Required()])
	submit = SubmitField('submit')




