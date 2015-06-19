from google.appengine.ext import ndb

def setup_func():
    """set up test fixtures"""
    ndb.get_context().set_cache_policy(False)

@ndb.transactional
def transactional_func():
    pass

def test_1():
    ndb.Key('foo', 'bar').delete()

def test_2():
    transactional_func()

test_1.nosegae_datastore_v3 = True
test_1.setup = setup_func
test_2.nosegae_datastore_v3 = True
test_2.setup = setup_func

