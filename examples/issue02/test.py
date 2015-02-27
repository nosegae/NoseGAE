from webtest import TestApp
from issue02 import app

app = TestApp(app)


def test_sys_modules_available():
    response = app.get('/')
    assert 'Hello world!' in str(response)
