from datetime import date

from project import db
from project.models import Task, User


db.create_all()


db.session.commit()

