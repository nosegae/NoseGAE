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

.. shell :: nosetests -v --with-gae
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

.. shell :: nosetests -v --with-gae
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

.. shell :: nosetests -v --with-gae
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