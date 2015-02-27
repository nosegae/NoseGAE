from webtest import TestApp
import unittest
from helloworld import app

app = TestApp(app)


class TestUserService(unittest.TestCase):
    nosegae_user = True
    nosegae_user_kwargs = dict(USER_EMAIL='nosegae@example.org')

    def test_index(self):
        # this will call get_current_user()
        response = app.get('/')
        self.assertIn('nosegae@example.org', response.body)
