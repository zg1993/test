#!/usr/bin/env python
#-*- coding: utf-8-*-


from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission


def permission_required(permission):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			if not current_user.can(permission):
				print('init 403')
				abort(403)
			return f(*args, **kwargs)
		return decorated_function
	return decorator


def admin_required(f):
	#print('init admin_required')
	return permission_required(Permission.ADMINISTER)(f)