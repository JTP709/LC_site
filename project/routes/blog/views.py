# /routes/blog/views.py

### Imports ###
import sys
sys.path.insert(0, '/vagrant/leandras_site/project/model/')
from model import Base, Blog
from connect import connect
from flask import render_template, Blueprint, request, redirect, url_for, session, make_response, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import json

### Config ###
blog_blueprint = Blueprint('blog', __name__, template_folder='templates')

### Database connection ###
def dbconnect():
	# Connect to the database
	con = connect()
	Base.metadata.bind = con
	# Creates a session
	DBSession = sessionmaker(bind=con)
	dbsession = DBSession()
	return dbsession

### routes ###
@blog_blueprint.route('/blog/<cat>')
def blog(cat):
	dbsession = dbconnect()
	if cat in {'all','general','crafting','baking','travel'}:
		if cat == 'all':
			posts = dbsession.query(Blog).filter_by(hidden=False, updated=True).order_by(Blog.bid.desc()).all()
		else:
			posts = dbsession.query(Blog).filter_by(hidden=False, updated=True, category=cat).order_by(Blog.bid.desc()).all()
		return render_template('blog.html', posts=posts)
	else:
		return render_template('404.html')

@blog_blueprint.route('/blog/<int:bid>')
def blog_post(bid):
	dbsession = dbconnect()
	post = dbsession.query(Blog).filter_by(bid=bid).order_by(Blog.pid.desc()).first()
	return render_template('blog_post.html', post=post)

@blog_blueprint.route('/blog/newest')
def blog_new():
	dbsession = dbconnect()
	post = dbsession.query(Blog).order_by(Blog.pid.desc()).first()
	return	render_template('blog_post.html', post=post)

@blog_blueprint.route('/blog/admin')
def blog_admin():
	dbsession = dbconnect()
	posts = dbsession.query(Blog).filter_by(updated=True).order_by(Blog.bid.desc()).all()
	return render_template('blog_admin.html', posts=posts)

@blog_blueprint.route('/blog/admin/add')
def blog_admin_add():
	return render_template('blog_admin_add.html')

@blog_blueprint.route('/blog/admin/edit/<int:id>')
def blog_admin_edit(id):
	dbsession = dbconnect()
	post = dbsession.query(Blog).filter_by(bid=id).order_by(Blog.pid.desc()).first()
	return render_template('blog_admin_edit.html', post=post)

@blog_blueprint.route('/blog/admin/alter/<action>/<int:id>', methods = ['POST'])
def blog_admin_alter(action,id):
	dbsession = dbconnect()
	if action == 'delete':
		post = dbsession.query(Blog).filter_by(bid = id).order_by(Blog.pid.desc()).first()
		post.hidden = True
		dbsession.commit()
		flash("Blog post #%s had been deleted." % id)
		return redirect(url_for('blog.blog_admin'))
	if action == 'undelete':
		post = dbsession.query(Blog).filter_by(bid = id).order_by(Blog.pid.desc()).first()
		post.hidden = False
		dbsession.commit()
		flash("Blog post #%s had been restored." % id)
		return redirect(url_for('blog.blog_admin'))
	if action == 'add':
		old_id = dbsession.query(Blog.bid).order_by(Blog.bid.desc()).first()
		new_id = old_id[0]+1
		title = request.form['title']
		sub_title = request.form['sub_title']
		author = 'Leandra Clifton'
		date_time = datetime.now()
		category = request.form['category']
		content = request.form['content']
		
		post = Blog(bid = new_id,
					title = title,
					sub_title = sub_title,
					author = author,
					date_time = date_time,
					category = category,
					content = content,
					hidden = False,
					updated = True)
		dbsession.add(post)
		dbsession.commit()
		flash("Blog post has been added.")
		return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
	if action == 'edit':
		o_post = dbsession.query(Blog).filter_by(bid = id).order_by(Blog.pid.desc()).first()
		o_post.updated = False
		dbsession.commit()

		title = request.form['title']
		sub_title = request.form['sub_title']
		author = 'Leandra Clifton'
		date_time = datetime.now()
		category = request.form['category']
		content = request.form['content']
		
		post = Blog(bid = id,
					title = title,
					sub_title = sub_title,
					author = author,
					date_time = date_time,
					category = category,
					content = content,
					hidden = False,
					updated = True)
		dbsession.add(post)
		dbsession.commit()
		flash("Blog post #%s has been edited." % id)
		return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 