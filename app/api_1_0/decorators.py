#!/usr/bin/env python
#-*- coding: utf-8-*-

from functools import wraps
from flask import g
from .errors import forbidden



def permission_required(permission):
	def decorator(f):
		@wraps(f)
		def decoreted_function(*args, **kwargs):
			if not g.current_user.can(permission):
				return forbidden('Insufficent permission')
			return f(*args, **kwargs)
		return decoreted_function
	return decorator