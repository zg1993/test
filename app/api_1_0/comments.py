#!/usr/bin/env python
#-*- coding: utf-8-*-  

from . import api
from ..models import Post
from ..models import Comment
from ..models import Permission
from .decorators import permission_required
from .. import db
from flask import jsonify
from flask import request
from flask import g
from flask import url_for


@api.route('/comments/<int:id>')
def get_comment(id):
	comment = Comment.query.get_or_404(id)
	return jsonify(comment.to_json())


@api.route('/comments/')
def get_comments():
	comments = Comment.query.order_by(Comment.timestamp.desc()).all()
	return jsonify({'comments': [comment.to_json() for comment in comments] })


@api.route('/posts/<int:id>/comments/')
def get_post_comments(id):
	post = Post.query.get_or_404(id)
	comments = post.comments.order_by(Comment.timestamp.desc()).all()
	return jsonify({'comments': [comment.to_json() for comment in comments]})



@api.route('/posts/<int:id>/comments/', methods=['POST'])
@permission_required(Permission.COMMENT)
def new_post_comment(id):
	post = Post.query.get_or_404(id)
	comment = Comment.from_json(request.json)
	comment.author = g.current_user
	comment.post = post
	db.session.add(comment)
	db.session.commit()
	return jsonify(comment.to_json()), 201, \
		{'Location': url_for('api.get_comment', id=comment.id, _external=True)}