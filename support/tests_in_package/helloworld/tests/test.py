from webtest import TestApp
import main

from nose.tools import eq_

app = TestApp(main.app)


def test_index():
    response = app.get('/')
    assert 'Hello world!' in str(response)
    eq_(1, 1, "Math is weird on your planet")
