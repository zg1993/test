#!/usr/bin/env python
#-*- coding: utf-8-*-


from flask import Blueprint
from ..models import Permission

# 蓝本中定义的路由处于休眠状态，直到蓝本注册到程序上后，路由才真正成为程序的一部分
# 在工厂函数中注册蓝本
main = Blueprint('main', __name__)

@main.app_context_processor
def inject_permission():
	return dict(Permission=Permission)


from . import views, errors