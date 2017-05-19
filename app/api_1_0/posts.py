#!/usr/bin/env python
#-*- coding: utf-8-*-


from . import api
from .errors import forbidden
from ..models import Post
from ..models import Permission
from .decorators import permission_required
from .. import db
from flask import jsonify
from flask import request
from flask import g
from flask import url_for
import pdb



@api.route('/posts/')
def get_posts():
	posts = Post.query.all()
	print('posts counts: {}'.format(posts.__len__()))
	#pdb.set_trace()
	return jsonify({'posts': [post.to_json() for post in posts] })


@api.route('/posts/<int:id>')
def get_post(id):
	#pdb.set_trace()
	post = Post.query.get_or_404(id)
	return jsonify(post.to_json())


@api.route('/posts/', methods=['POST'])
@permission_required(Permission.WRITE_ARTICLES)
def new_post():
	#pdb.set_trace()
	print('new_post....typeof(request.json): {}'.format(request.json))
	post = Post.from_json(request.json)
	post.au = g.current_user
	db.session.add(post)
	db.session.commit()
	return jsonify(post.to_json()), 201, {'Location': url_for('api.get_post', id=post.id, _external=True)}


@api.route('/posts/<int:id>', methods=['PUT'])
@permission_required(Permission.WRITE_ARTICLES)
def edit_post(id):
	post = Post.query.get_or_404(id)
	if g.current_user != post.author and \
			not g.current_user.can(Permission.ADMINISTER):
		return forbidden('Insufficient permission')
	post.body = request.json.get('body', post.body)
	db.session.add(post)
	return jsonify(post.to_json())