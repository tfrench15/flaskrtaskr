import os
import unittest

from views import app, db
from _config import basedir
from models import User
from test_helpers import AllHelpers

TEST_DB = 'test.db'


class TestUsers(unittest.TestCase):

	def test_user_setup(self):
		new_user = User("tim", "tim@tpfrench.com", "timfrench")
		db.session.add(new_user)
		db.session.commit()
		test = db.session.query(User).all()
		for t in test:
			t.name 
		assert t.name == "tim"

	def test_form_is_present(self):
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Please login to access your task list', response.data)

	
	def test_users_cannot_login_unless_registered(self):
		response = self.login('foo', 'bar')
		self.assertIn(b'Invalid username or password', response.data)


	def test_users_can_login(self):
		self.register("tim", "tim@tpfrench.com", "helloworld", "helloworld")
		response = self.login('tim', 'helloworld')
		self.assertIn(b'Welcome', response.data)

	def test_invalid_form_data(self):
		self.register("tim", "tim@tpfrench.com", "helloworld", "helloworld")
		response = self.login('alert("alert box!");', 'foo')
		self.assertIn(b'Invalid username or password', response.data)

	def test_form_is_present_on_register_page(self):
		response = self.app.get('register/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Please register to access the task list', response.data)

	def test_user_registration(self):
		self.app.get('register/', follow_redirects = True)
		response = self.register(
			'tim',
			'tim@tpfrench.com',
			'helloworld',
			'helloworld'
		)
		self.assertIn(b'Please register to access the task list', response.data)


	def test_logged_in_users_can_logout(self):
		self.register('Amanda', 'amandabfrench@gmail.com', 'camelback', 'camelback')
		self.login('Amanda', 'camelback')
		response = self.logout()
		self.assertIn(b'Goodbye', response.data)

	def test_not_logged_in_users_cannot_logout(self):
		response = self.logout()
		self.assertNotIn(b'Goodbye', response.data)

	def test_default_user_role(self):
		db.session.add(
			User(
				"Johnny",
				'john@doe.com',
				"johnny"
				)
			)
		db.session.commit()

		users = db.session.query(User).all()
		print(users)
		for user in users:
			self.assertEquals(user.role, 'user')