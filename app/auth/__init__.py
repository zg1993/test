#!/usr/bin/env python
#-*- coding: utf-8-*-


from flask import Blueprint

# auth蓝本对象的添加
auth = Blueprint('auth', __name__)


from . import views