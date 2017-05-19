#!/usr/bin/env python
#-*- coding: utf-8-*-

import pdb
import os 
#--coverage
COV = None
#pdb.set_trace()
if os.environ.get('FLASK_COVERAGE'):
	#pdb.set_trace()
	import coverage
	COV = coverage.coverage(branch=True, include='app/*')
	COV.start()


from app import create_app
from app import db
from app.models import User, Role, Post, Follow, Comment, Permission
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask import url_for
from flask import current_app
import pdb


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
#pdb.set_trace()
manager = Manager(app)
migrate = Migrate(app, db)

def make_shell_context():
	return dict(app=app, db=db, User=User, Role=Role,
			Post=Post, Follow=Follow, Comment=Comment, Permission=Permission, url_for=url_for, current_app=current_app)


@manager.command
def test(coverage=False):
	''' Run the unit tests.'''
	if coverage and not os.environ.get('FLASK_COVERAGE'):
		import sys
		os.environ['FLASK_COVERAGE'] = '1'
		os.execvp(sys.executable, [sys.executable] + sys.argv)
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)
	if COV:
		#COV.stop()
		COV.save()
		print('Coverage Sunmmary:')
		COV.report()
		basedir = os.path.abspath(os.path.dirname(__file__))
		covdir = os.path.join(basedir, 'tmp/coverage')
		COV.html_report(directory=covdir)
		print('HTML version: file://%s/index.html' % covdir)
		COV.erase()


@manager.command
def profile(length=25, profile_dir=None):
	"""Start the application under the code profiler."""
	from werkzeug.contrib.profiler import ProfilerMiddleware
	app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[length], profile_dir=profile_dir)
	app.run()


@manager.command
def deploy():
	"""Run deployment tasks."""
	from flask_migrate import upgrade
	
	upgrade()
	Role.insert_roles()
	User.add_self_follows()
	
	
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
	manager.run()



























