#!/usr/bin/env python
#-*- coding: utf-8-*-


from . import api
from ..models import Post
from ..models import User
#from ..models import Permission
#from .decorators import permission_required
#from .. import db
from flask import jsonify
#from flask import request
#from flask import g
import pdb


@api.route('/users/<int:id>')
def get_user(id):
	user = User.query.get_or_404(id)
	#pdb.set_trace()
	return jsonify(user.to_json())


@api.route('/users/<int:id>/posts/')
def get_user_posts(id):
	user = User.query.get_or_404(id)
	posts = user.posts.order_by(Post.timestamp.desc()).all()
	return jsonify({'posts': [post.to_json() for post in posts] })


@api.route('/users/<int:id>/timeline/')
def get_user_followed_posts(id):
	user = User.query.get_or_404(id)
	followed = user.followed_posts.order_by(Post.timestamp.desc()).all()
	return jsonify({'posts': [post.to_json() for post in posts] })

	
