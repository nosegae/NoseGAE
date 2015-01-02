from webtest import TestApp
from main import app

app = TestApp(app)


def test_that_fails():
    response = app.get('/')
    assert response


test_that_fails.nosegae_logservice = True
