from datetime import date

from project import db
from project.models import Task, User


db.create_all()

db.session.add(
	User("admin, ad@min.com", "admin", "admin")
)
db.session.add(
	Task("Finish this tutorial", date(2017, 12, 31), 10, date(2017, 12, 31), 1, 1)
)
db.session.add(
	Task("Finish RealPython", date(2018, 01, 31), 10, date(2018, 01, 31), 1, 1)
)
db.session.commit()

