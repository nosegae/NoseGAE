from webtest import TestApp
from issue02 import application

app = TestApp(application())

def test_index():
    response = app.get('/')
    assert 'Hello world!' in str(response)
