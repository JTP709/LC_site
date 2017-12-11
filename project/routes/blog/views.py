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
@blog_blueprint.route('/blog')
def blog():
	dbsession = dbconnect()
	posts = dbsession.query(Blog.title,
							Blog.author,
							func.to_char(Blog.date_time, 'FMMonth FMDD, YYYY'),
							func.to_char(Blog.date_time, 'HH24:MI'),
							Blog.category,
							Blog.content).filter_by(hidden=False).order_by(Blog.bid.desc()).all()
	length = len(posts)
	return render_template('blog.html', posts=posts, length=length)

@blog_blueprint.route('/blog/<int:id>')
def blog_post(id):
	dbsession = dbconnect()
	post = dbsession.query(Blog.title,
							Blog.author,
							func.to_char(Blog.date_time, 'FMMonth FMDD, YYYY'),
							func.to_char(Blog.date_time, 'HH24:MI'),
							Blog.category,
							Blog.content).filter_by(id=id).one()
	print(post)
	return render_template('blog_post.html', post=post)

@blog_blueprint.route('/blog/admin')
def blog_admin():
	dbsession = dbconnect()
	posts = dbsession.query(Blog.bid,
							Blog.title,
							Blog.author,
							func.to_char(Blog.date_time, 'FMMonth FMDD, YYYY'),
							func.to_char(Blog.date_time, 'HH24:MI'),
							Blog.category,
							Blog.hidden).order_by(Blog.bid.desc()).all()
	length = len(posts)
	return render_template('blog_admin.html', posts=posts, length=length)

@blog_blueprint.route('/blog/admin/add', methods = ['GET', 'POST'])
def blog_admin_add():
	if request.method == 'POST':
		# add new blog
		dbsession = dbconnect()
		old_id = dbsession.query(Blog.id).order_by(Blog.id.desc()).first()
		new_id = old_id[0]+1
		time = dbsession.query(Blog.date_time).first()
		title = request.form['title']
		author = 'Leandra Clifton'
		date_time = datetime.now()
		category = request.form['category']
		content = request.form['content']
		post = Blog(bid = new_id,
					title = title,
					author = author,
					date_time = date_time,
					category = category,
					content = content)
		dbsession.add(post)
		dbsession.commit()
		return redirect(url_for('blog.blog'))
	else:
		return render_template('blog_admin_add.html')

@blog_blueprint.route('/blog/admin/alter/<action>/<int:id>', methods = ['POST'])
def blog_admin_del(action,id):
	dbsession = dbconnect()
	post = dbsession.query(Blog).filter_by(bid = id).first()
	if action == 'delete':
		post.hidden = True
		dbsession.commit()
		flash("Blog post #%s had been deleted." % id)
	if action == 'undelete':
		post.hidden = False
		dbsession.commit()
		flash("Blog post #%s had been restored." % id)
	return redirect(url_for('blog.blog_admin'))