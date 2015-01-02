from webtest import TestApp
import helloworld
import os


def test_index():
    test_index.testbed.init_taskqueue_stub(task_retry_seconds=42, root_path=os.path.dirname(__file__))
    app = TestApp(helloworld.app)
    # fires off a task queue and should pass without exceptions
    response = app.get('/')
    assert 'Hello world!' in str(response)
