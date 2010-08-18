from webtest import TestApp
from helloworld import application

app = TestApp(application())

def test_index():
    # fires off a task queue and should pass without exceptions
    response = app.get('/')
    assert 'Hello world!' in str(response)
