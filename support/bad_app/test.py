print "===================== test code ======================"
from webtest import TestApp
from bad_app import application
from bisect import bisect
print bisect



app = TestApp(application())

def test_writing():
    response = app.get('/')
    assert 'Hello' in str(response)
print "========================== end test code ======================"
