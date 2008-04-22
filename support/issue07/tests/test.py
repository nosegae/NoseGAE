from webtest import TestApp
from helloworld import application
from nose.tools import eq_

app = TestApp(application())

def test_index():
    response = app.get('/')
    assert 'Hello world!' in str(response)
    eq_(1, 1, "Math is weird on your planet")
