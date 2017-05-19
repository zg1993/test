#!/usr/bin/env python
#-*- coding: utf-8-*-


import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'shengming'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	MAIL_SERVER = 'smtp.kiyozawa.com'
	MAIL_PORT = 25
	MAIL_USE_TLS = False
	# MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	# MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	MAIL_USERNAME = 'zhougang@kiyozawa.com'
	MAIL_PASSWORD = '222222Zz'
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	FLASKY_MAIL_SENDER = 'zhougang@kiyozawa.com'
	FLASKY_ADMIN = 'zg@kiyozawa.com'
	FLASK_POSTS_PER_PAGE = 10
	FLASK_COMMENTS_PER_PAGE = 15
	#SQL record querues
	SQLALCHEMY_RECORD_QUERIES = True
	FLASKY_SLOW_DB_QUERY_TIME = 0.5

	SSL_DISABLE = True


	@staticmethod
	def init_app(app):
		pass


class DevelopmentConfig(Config):
	DEBUG = True

	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
	TESTING = True
	#testing model forbid CSRF projected
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'data.sqlite')
	#testing model forbid CSRF projected
	#WTF_CSRF_ENABLED = False


	@classmethod
	def init_app(cls, app):
		Config.init_app(app)

		import logging
		from logging.handlers import SMTPHandler
		credentials = None
		secure = None
		if getattr(cls, 'MAIL_USERNAME', None) is not None:
			credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
			if getattr(cls, 'MAIL_USE_TLS', None):
				secure = ()
		mail_handler = SMTPHandler(
			mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
			fromaddr=cls.FLASKY_MAIL_SENDER,
			toaddrs=[cls.FLASKY_ADMIN],
			subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + ' Application Error',
			credentials=credentials,
			secure=secure)
		mail_handler.setLevel(logging.ERROR)
		app.logger.addHandler(mail_handler)


class HerokuConfig(ProductionConfig):
	SSL_DISABLE = bool(os.environ.get('SSL_DISABLE'))

	@classmethod
	def init_app(cls, app):
		ProductionConfig.init_app(app)

		from werkzeug.contrib.fixers import ProxyFix
		app.wsgi_app = ProxyFix(app.wsgi_app)

		import logging
		from logging import StreamHandler
		file_handler = StreamHandler()
		file_handler.setLevel(logging.WARNING)
		app.logger.addHandler(file_handler)
		

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'heroku': HerokuConfig,

	'default': DevelopmentConfig
}
