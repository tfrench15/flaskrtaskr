import os
import unittest

from views import app, db
from _config import basedir
from models import User
from test_helpers import AllHelpers

TEST_DB = 'test.db'

class TestTasks(unittest.TestCase):

	def test_logged_in_users_can_access_tasks(self):
		self.register('Amanda', 'amandabfrench@gmail.com', 'camelback', 'camelback')
		self.login('Amanda', 'camelback')
		response = self.app.get('tasks/')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Add a new task', response.data)

	def test_not_logged_in_users_cannot_access_tasks_page(self):
		response = self.app.get('tasks/', follow_redirects = True)
		self.assertIn(b'You need to login first', response.data)

	def test_users_can_add_tasks(self):
		self.create_user('Amanda', 'amandabfrench@gmail.com', 'camelback')
		self.login('Amanda', 'camelback')
		self.app.get('tasks/', follow_redirects = True)
		response = self.create_task()
		self.assertIn(b'New entry was successfully posted', response.data)

	def test_users_cannot_add_task_when_error(self):
		self.create_user('Amanda', 'amandabfrench@gmail.com', 'camelback')
		self.login('Amanda', 'camelback')
		self.app.get('tasks/', follow_redirects = True)
		response = self.app.post('add/', data = dict(
			name = 'Go to the bank', 
			due_date = '',
			priority = '1',
			posted_date = '12/24/2017',
			status = '1'
		), follow_redirects = True)
		self.assertIn(b'This field is required', response.data)

	def test_users_can_complete_tasks(self):
		self.create_user('Amanda', 'amandabfrench@gmail.com', 'camelback')
		self.login('Amanda', 'password')
		self.app.get('tasks/', follow_redirects = True)
		self.create_task()
		response = self.app.get("complete/1/", follow_redirects = True)
		self.assertIn(b'The task is complete', response.data)

	def test_users_can_delete_tasks(self):
		self.create_user('Amanda', 'amandabfrench@gmail.com', 'camelback')
		self.login('Amanda', 'password')
		self.app.get('tasks/', follow_redirects = True)
		self.create_task()
		response = self.app.get("delete/1/", follow_redirects = True)
		self.assertIn(b'The task was deleted', response.data)

	def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
		self.create_user('Amanda', 'amandabfrench@gmail.com', 'camelback')
		self.login('Amanda', 'camelback')
		self.app.get('tasks/', follow_redirects = True)
		self.create_task()
		self.logout()
		self.create_user('Jenn', 'jennfrench@gmail.com', 'hoboken')
		self.login('Jenn', 'hoboken')
		self.app.get('tasks/', follow_redirects = True)
		response = self.app.get("complete/1/", follow_redirects = True)
		self.assertNotIn(b'The task is complete', response.data)
		self.assertIn(b'You can only update tasks that belong to you', response.data)

	def test_users_cannot_delete_tasks_that_are_not_created_by_them(self):
		self.create_user('Amanda', 'amandabfrench@gmail.com', 'camelback')
		self.login('Amanda', 'camelback')
		self.app.get('tasks/', follow_redirects = True)
		self.create_task()
		self.logout()
		self.create_user('Jenn', 'jennfrench@gmail.com', 'hoboken')
		self.login('Jenn', 'hoboken')
		self.app.get('tasks/', follow_redirects = True)
		response = self.app.get("delete/1/", follow_redirects = True)
		self.assertNotIn(b'The task was deleted', response.data)
		self.assertIn(b'You can only delete tasks that belong to you', response.data)

	def test_admin_users_can_complete_tasks_that_are_not_created_by_them(self):
		self.create_user('Amanda', 'amandabfrench@gmail.com', 'camelback')
		self.login('Amanda', 'camelback')
		self.app.get('/tasks', follow_redirects = True)
		self.create_task()
		self.logout()
		self.create_admin_user()
		self.login('Superman', 'allpowerful')
		self.app.get('tasks/', follow_redirects = True)
		response = self.app.get("delete/1/", follow_redirects = True)
		self.assertNotIn(b'You can only update tasks that belong to you', response.data)

	


