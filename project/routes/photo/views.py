# /routes/photo/views.py

### Imports ###
from flask import render_template, Blueprint

### Config ###
photo_blueprint = Blueprint('photo', __name__, template_folder='templates')

### routes ###
@photo_blueprint.route('/photo')
def photo():
	return render_template('photos.html')