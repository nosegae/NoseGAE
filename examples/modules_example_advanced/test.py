import unittest
from webtest import TestApp
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'default'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'mobile'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'static'))
import helloworld
import mobile
import printenv


class TestModules(unittest.TestCase):

    nosegae_taskqueue = True
    nosegae_modules = True
    nosegae_user = True
    nosegae_user_kwargs = {
        'USER_IS_ADMIN': '1',
        'USER_EMAIL': 'josh@example.org'
    }

    def test_frontend(self):
        """Tests the main module in app.yaml which adds an item to the taskqueue that runs on static backend"""
        frontend = TestApp(helloworld.APP)
        response = frontend.get('/')
        self.assertEqual(response.content_type, 'text/plain')
        self.assertIn('Hello, webapp2 World!', response.body)

    def test_mobile_frontend(self):
        mobile_frontend = TestApp(mobile.APP)
        response = mobile_frontend.get('/mobile/')
        self.assertEqual(response.content_type, 'text/html')
        self.assertIn('josh@example.org', response.body)

    def test_static_backend(self):
        work = TestApp(printenv.APP)
        response = work.get('/work/')
        self.assertEqual(response.content_type, 'text/html')
        self.assertIn('josh@example.org', response.body)
