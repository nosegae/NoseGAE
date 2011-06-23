---------------------------------------------------
NoseGAE: Test support for Google Application Engine
---------------------------------------------------

.. fixtures :: fixt
.. contents ::

Overview
========

NoseGAE is a nose_ plugin that makes it easier to write functional and unit
tests for `Google App Engine`_ applications.

When the plugin is installed, you can activate it by using the
``--with-gae`` command line option. The plugin also includes an option
for setting the path to the Google App Engine python library, if it is
not in the standard location of ``/usr/local/google_appengine``.

What does it do?
================

Functional tests
~~~~~~~~~~~~~~~~

The plugin sets up the GAE development environment before your test
run. This means that you can easily write functional tests for your
application without having to actually start the dev server and test
over http. **Note** however that this kind of testing requires that
your application be a wsgi_ application.

Consider a simple hello world wsgi application:

.. include :: support/helloworld/helloworld.py
   :literal:

And a simple functional test suite for the application:

.. include :: support/helloworld/test.py
   :literal:

The important part to note is the `application()` function that
returns the application. That function provides a way get the
application under test and call it directly, without having to pass
through the dev app server. And that's all you need to do for basic
functional testing.

.. shell :: nosetests-2.5 -v --with-gae
   :cwd: support/helloworld
   :post: cleanup
   :stderr:

   test.test_index ... ok
   <BLANKLINE>
   ----------------------------------------------------------------------
   Ran 1 test in ...s
   <BLANKLINE>
   OK
..

Unit tests
~~~~~~~~~~

Functional tests are only one kind of test, of course. What if you
want to write unit tests for your data models? Normally, you can't use
your models at all outside of the dev environment, because the Google
App Engine datastore isn't available. However, since the NoseGAE
plugin sets up the development environment around your test run, you
can use models directly in your tests.

Consider a simple models.py file that includes some doctests:

.. include:: support/pets/models.py
   :literal:

Without NoseGAE, the doctests fail.

.. shell :: nosetests-2.5 -v --with-doctest
   :cwd: support/pets
   :post: cleanup
   :stderr:

   Failure: ImportError (No module named google.appengine.ext) ... ERROR
   <BLANKLINE>
   ======================================================================
   ERROR: Failure: ImportError (No module named google.appengine.ext)
   ----------------------------------------------------------------------
   Traceback (most recent call last):
   ...
   ImportError: No module named google.appengine.ext
   <BLANKLINE>
   ----------------------------------------------------------------------
   Ran 1 test in ...s
   <BLANKLINE>
   FAILED (errors=1)
..
     
With NoseGAE, they pass.

.. shell :: nosetests-2.5 -v --with-doctest --with-gae
   :cwd: support/pets
   :post: cleanup
   :stderr:

   Doctest: models.Pet ... ok
   <BLANKLINE>
   ----------------------------------------------------------------------
   Ran 1 test in ...s
   <BLANKLINE>
   OK
..

Realism in testing
==================

Besides the dev appserver and the datastore, the main sticking point
for testing Google App Engine applications is the highly restrictive
runtime environment. When you test without NoseGAE, tests that should
fail (because the tested code **will fail** when run inside the Google
App Engine) may pass.

For instance, consider an app that uses the `socket` module, like this one:

.. include :: support/bad_app/bad_app.py
   :literal:

With a simple functional test:

.. include :: support/bad_app/test.py
   :literal:

This test will pass when run outside of the Google App Engine
environment.
 
.. shell :: nosetests-2.5 -v
   :cwd: support/bad_app
   :post: cleanup
   :stderr:

   test.test_index_calls_gethostbyname ... ok
   <BLANKLINE>
   ----------------------------------------------------------------------
   Ran 1 test in ...s
   <BLANKLINE>
   OK
..
    
When run with NoseGAE, it will fail, as it should.

.. shell :: nosetests-2.5 -v --with-gae
   :cwd: support/bad_app
   :post: cleanup
   :stderr:

   test.test_index_calls_gethostbyname ... ERROR
   <BLANKLINE>
   ======================================================================
   ERROR: test.test_index_calls_gethostbyname
   ----------------------------------------------------------------------
   Traceback (most recent call last):
   ...
   <BLANKLINE>
   ----------------------------------------------------------------------
   Ran 1 test in ...s
   <BLANKLINE>
   FAILED (errors=1)
..
    
It is important to note that only **application** code is sandboxed by
NoseGAE. Test code imports outside of the sandbox, so your test code has full
access to the system and available python libraries, including the Google App
Engine datastore and other Google App Engine libraries.

For this reason, **file access is not restricted** in the same way as it
is under GAE, because it is impossible to differentiate application code file
access from test code file access.

However, this means that some things like profiling or Nose's --coverage option 
will not work without some hacks.  If you run into these issues you can pass in 
the option --without-sandbox to turn off the GAE import hook simulation.

.. _nose : http://somethingaboutorange.com/mrl/projects/nose/
.. _`google app engine` : http://code.google.com/appengine/
.. _wsgi : http://www.wsgi.org/wsgi

Developers
==========

To work on NoseGAE you'll need some dependencies.  Unfortunately, the Google App Engine SDK makes virtualenv unusable so you either have to pollute your global Python or build a custom Python 2.5 interpreter for use with NoseGAE (recommended).

* Install setuptools
* easy_install Nose trestle WebTest

Run the tests::

  # Set this to the top level dir, the one with the bin dir in it:
  export PY25_ROOT=/usr/local/python2.5.5-app-engine
  ./run_tests.sh

