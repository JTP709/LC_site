# /routes/landing/views.py

### Imports ###
from flask import render_template, Blueprint

### Config ###
landing_blueprint = Blueprint('landing', __name__, template_folder='templates')

### routes ###
@landing_blueprint.route('/')
def index():
	return render_template('index.html')