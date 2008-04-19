from webtest import TestApp
from bad_app import application
import socket

app = TestApp(application())

def test_index_calls_gethostbyname():
    # this works, because in test code GAE sandbox is not active
    host = socket.gethostbyname('localhost')
    response = app.get('/')
    assert 'Hello' in str(response)
    assert host in str(response)
