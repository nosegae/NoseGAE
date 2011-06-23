More tests
----------

.. fixtures :: fixt

This document contains edge-case tests that don't add anything to the
end-user documentation.

Bugs
====

Issue 2
^^^^^^^

sys.modules should be available inside the sandbox.

.. shell :: nosetests-2.5 -v --with-gae
   :cwd: support/issue02
   :post: cleanup
   :stderr:

   test.test_sys_modules_available ... ok
   <BLANKLINE>
   ----------------------------------------------------------------------
   Ran 1 test in ...s
   <BLANKLINE>
   OK
..

Tests in packages
^^^^^^^^^^^^^^^^^

You can organize your files with tests under the main app package, like this::

  .
  |-- app.yaml
  |-- helloworld
  |   |-- __init__.py
  |   `-- tests
  |       |-- __init__.py
  |       |-- test.py
  |-- index.yaml
  `-- main.py

And the test package and modules under it will be outside the sandbox.

.. shell :: nosetests-2.5 -v --with-gae
   :cwd: support/tests_in_package
   :post: cleanup
   :stderr:

   helloworld.tests.test.test_index ... ok
   <BLANKLINE>
   ----------------------------------------------------------------------
   Ran 1 test in ...s
   <BLANKLINE>
   OK
..

Issue 7
^^^^^^^

The modules loaded by any sandboxed module are added to the shared module set,
so that they persist between entries into the sandbox. This prevents weird
import errors when you have more than one test module, one of which imports a
module from a sandboxed package.

.. shell :: nosetests-2.5 -v --with-gae
   :cwd: support/issue07
   :post: cleanup
   :stderr:

   tests.test.test_index ... ok
   tests.test_models.test ... ok
   <BLANKLINE>
   ----------------------------------------------------------------------
   Ran 2 tests in ...s
   <BLANKLINE>
   OK
..

Test that logging still works
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After SDK 1.2.5 dev_appserver got a bit more aggressive about adding log handlers.
NoseGAE has to silence the logs and this makes sure logging still works from apps.
See Issue 25 for details.  NOTE: I'm not sure what the "strop" import error is about.

.. shell :: nosetests-2.5 -v --with-gae
   :cwd: support/app_with_logging
   :post: cleanup
   :stderr:

   tests.test.test_that_fails ... FAIL
   <BLANKLINE>
   ======================================================================
   FAIL: tests.test.test_that_fails
   ----------------------------------------------------------------------
   Traceback (most recent call last):
   ...
   AssertionError: this fails so that logging output can be inspected
   ...
   root: INFO: I saw a penguin at the zoo and it told me a secret.
   <BLANKLINE>
   ----------------------------------------------------------------------
   Ran 1 test in ...s
   <BLANKLINE>
   FAILED (failures=1) 
..


Issue 42 - Task Queues
^^^^^^^^^^^^^^^^^^^^^^

Create a test outside the app-engine path using some taskqueue facility (for e.g. a task queue with another name than 'default'). Running those tests with nose even with --gae-application set correctly they will fail, telling you that said queue isn't existing.

Without the fix in NoseGAE which involves setting up the root path for queue storage, the UnknownQueueError exception will be raised.

.. shell :: nosetests-2.5 -v --with-gae
   :cwd: support/issue42_task-queue
   :post: cleanup
   :stderr:

   test.test_index ... ok
   <BLANKLINE>
   ----------------------------------------------------------------------
   Ran 1 test in ...s
   <BLANKLINE>
   OK
..

Issue 13 - users.get_current_user() not working
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Create an app that calls users.get_current_user() -- it fails because the stubs did not set up the environ.

.. shell :: nosetests-2.5 -v --with-gae
   :cwd: support/issue13-get_current_user
   :post: cleanup
   :stderr:

   test.test_index ... ok
   <BLANKLINE>
   ----------------------------------------------------------------------
   Ran 1 test in ...s
   <BLANKLINE>
   OK
..

