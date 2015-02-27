from webtest import TestApp
import unittest
import helloworld

app = TestApp(helloworld.app)


class HelloWorldTest(unittest.TestCase):
    def test_index(self):
        """Tests that the index page for the application

        The page should be served as: Content-Type: text/plain
        The body content should contain the string: Hello world!
        """
        response = app.get('/')
        self.assertEqual(response.content_type, 'text/plain')
        self.assertIn('Hello world!', response.body)
