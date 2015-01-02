from webtest import TestApp
from helloworld import app
import os

app = TestApp(app)


def test_index():
    # fires off a task queue and should pass without exceptions
    response = app.get('/')
    assert 'Hello world!' in str(response)

# Enable any stubs needed as attributes off of the test function

# NoseGAE looks for queue.yaml in the root of the
# application when nosegae_taskqueue is True
test_index.nosegae_taskqueue = True

# ...or you can manually set the path and any additional arguments with the kwargs attribute
test_index.nosegae_taskqueue_kwargs = dict(task_retry_seconds=42, root_path=os.path.dirname(__file__))
