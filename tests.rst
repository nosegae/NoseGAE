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
