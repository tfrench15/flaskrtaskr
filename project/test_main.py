import os
import unittest

from project import app, db
from project._config import basedir
from project.models import User

TEST_DB = 'test.db'

class MainTests(unittest.TestCase):

	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['DEBUG'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
		self.app = app.test_client()
		db.create_all()

		self.assertEquals(app.debug, False)

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def login(self, name, password):
		return self.app.post('/', data = dict(name = name, password = password), follow_redirects = True)

	def test_404_error(self):
		response = self.app.get('/this-route-does-not-exist')
		self.assertEquals(response.status_code, 404)
		self.assertIn(b'Sorry. There\'s nothing here.', response.data)

	def test_500_error(self):
		bad_user = User(
			name = 'Amanda',
			email = 'amandabfrench@gmail.com',
			password = 'django',
			)
		db.session.add(bad_user)
		db.session.commit()
		self.assertRaises(ValueError, self.login, 'Amanda', 'django')
		try:
			response = self.login('Amanda', 'django')
			self.assertEquals(response.status_code, 500)
		except ValueError:
			pass

	def test_index(self):
		response = self.app.get('/', content_type = 'html/text')
		self.assertEquals(response.status_code, 200)

		

if __name__ == "__main__":
	unittest.main()