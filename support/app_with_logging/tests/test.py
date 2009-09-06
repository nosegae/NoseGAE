from webtest import TestApp
from helloworld import application
from nose.tools import eq_

app = TestApp(application())

def test_that_fails():
    response = app.get('/')
    assert 'Hello world!' in str(response)
    assert 0, "this fails so that logging output can be inspected"
