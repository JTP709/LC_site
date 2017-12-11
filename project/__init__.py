### Imports ###
from flask import Flask

### Config ###
app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

### Blueprints ###
from project.routes.landing.views import landing_blueprint
from project.routes.blog.views import blog_blueprint
from project.routes.photo.views import photo_blueprint

# register the blueprints
app.register_blueprint(landing_blueprint)
app.register_blueprint(blog_blueprint)
app.register_blueprint(photo_blueprint)