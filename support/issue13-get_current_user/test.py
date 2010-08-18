from webtest import TestApp
from helloworld import application

app = TestApp(application())

def test_index():
    # this will call get_current_user()
    response = app.get('/')
    assert 'Hello world!' in str(response)
