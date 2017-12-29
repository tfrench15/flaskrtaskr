from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 


app = Flask(__name__)
app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.users.tasks import tasks_blueprint

app.register_blueprint(users_blueprint)
app.register_blueprint(tasks_blueprint)