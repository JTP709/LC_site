# /routes/blog/views.py

### Imports ###
import sys
sys.path.insert(0, '/vagrant/leandras_site/project/model/')
from model import Base, Blog
from connect import connect
from flask import render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker

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
							Blog.content).order_by(Blog.id.desc()).all()
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
	return render_template('blog_admin.html')

@blog_blueprint.route('/blog/admin/add')
def blog_admin_add():
	return render_template('blog_admin_add.html')

@blog_blueprint.route('/blog/admin/delete/<int:id>')
def blog_admin_del(id):
	return render_template('blog_admin_del.html')