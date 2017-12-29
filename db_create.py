from datetime import date

from project import db
from project.models import Task, User


db.create_all()

db.session.add(
	User("admin, ad@min.com", "admin", "admin")
)
db.session.add(
	Task("Finish this tutorial", date(2017, 12, 31), 10, 1, 1, date(2018, 1, 31))
)
db.session.add(
	Task("Finish RealPython", date(2018, 1, 31), 10, 1, 1, date(2018, 1, 31))
)
db.session.commit()

