# /routes/landing/views.py

### Imports ###
import sys
sys.path.insert(0, '/vagrant/leandras_site/project/model/')
import re
from model import Base, Blog
from connect import connect
from flask import render_template, Blueprint, request, redirect, url_for, session, make_response, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker

### Config ###
landing_blueprint = Blueprint('landing', __name__, template_folder='templates')

### Database connection ###
def dbconnect():
	# Connect to the database
	con = connect()
	Base.metadata.bind = con
	# Creates a session
	DBSession = sessionmaker(bind=con)
	dbsession = DBSession()
	return dbsession

### Clean HTML from String ###
def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext

### routes ###
@landing_blueprint.route('/')
def index():
	dbsession = dbconnect()
	# Blog Previews
	crafting_post = dbsession.query(Blog).filter_by(hidden=False, updated=True, category='crafting').order_by(Blog.bid.desc()).first()
	crafting_post_preview = cleanhtml(crafting_post.content[1:500])+'...'
	baking_post = dbsession.query(Blog).filter_by(hidden=False, updated=True, category='baking').order_by(Blog.bid.desc()).first()
	baking_post_preview = cleanhtml(baking_post.content[1:500])+'...'
	travel_post = dbsession.query(Blog).filter_by(hidden=False, updated=True, category='travel').order_by(Blog.bid.desc()).first()
	travel_post_preview = cleanhtml(travel_post.content[1:500])+'...'
	general_post = dbsession.query(Blog).filter_by(hidden=False, updated=True, category='general').order_by(Blog.bid.desc()).first()
	general_post_preview = cleanhtml(general_post.content[1:500])+'...'
	return render_template('index.html', 
						   crafting_post=crafting_post,
						   crafting_post_preview=crafting_post_preview, 
						   baking_post=baking_post,
						   baking_post_preview=baking_post_preview, 
						   travel_post=crafting_post,
						   travel_post_preview=travel_post_preview, 
						   general_post=general_post,
						   general_post_preview=general_post_preview
						   )

@landing_blueprint.route('/admin')
def index_admin():
	return render_template('index_admin.html')