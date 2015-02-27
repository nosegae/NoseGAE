import unittest
from webtest import TestApp
import helloworld
import printenv


class TestModules(unittest.TestCase):

    nosegae_modules = True
    nosegae_user = True
    nosegae_user_kwargs = {
        'USER_IS_ADMIN': '1',
        'USER_EMAIL': 'josh@example.org'
    }

    def test_frontend(self):
        """Tests the main module in app.yaml"""
        frontend = TestApp(helloworld.APP)
        response = frontend.get('/')
        self.assertEqual(response.content_type, 'text/plain')
        self.assertIn('Hello, webapp2 World!', response.body)

    def test_mobile_frontend(self):
        mobile = TestApp(printenv.APP)
        response = mobile.get('/mobile/')
        self.assertEqual(response.content_type, 'text/html')
        self.assertIn('josh@example.org', response.body)

    def test_static_backend(self):
        work = TestApp(printenv.APP)
        response = work.get('/work/')
        self.assertEqual(response.content_type, 'text/html')
        self.assertIn('josh@example.org', response.body)
