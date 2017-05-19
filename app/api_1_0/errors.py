#!/usr/bin/env python
#-*- coding: utf-8-*-


from . import api
from app.exceptions import ValidationError
from flask import jsonify


def forbidden(message):
	response = jsonify({'error': 'forbidden', 'message': message})
	response.status_code = 403
	return response


def unauthorized(message):
	response = jsonify({'error': 'unauthorized', 'message': message})
	response.status_code = 401
	return response


@api.errorhandler(ValidationError)
def validation_error(e):
	return bad_request(e.args[0])






