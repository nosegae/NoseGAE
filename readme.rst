---------------------------------------------------
NoseGAE: Test support for Google Application Engine
---------------------------------------------------

.. contents ::

Overview
========

NoseGAE is a nose_ plugin that makes it easier to write unit tests for
`Google App Engine`_ applications.

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

    >>> import os
    >>> support = os.path.join(os.path.dirname(os.path.realpath(__file__)),
    ...                        'support')
    >>> hello_app = os.path.join(support, 'helloworld')
    >>> from nose.plugins.plugintest import run
    >>> from nosegae import NoseGAE
    >>> run(argv=['nosegae', '--with-gae', '--gae-application', hello_app,
    ...           '-v', hello_app], plugins=[NoseGAE()])
    test.test_index ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    OK

Unit tests
~~~~~~~~~~

Functional tests are only one kind of test, of course. What if you
want to write unit tests for your data models? Normally, you can't use
your models at all outside of the dev environment, because the Google
App Engine datastore isn't available. However, since the NoseGAE
plugin sets up the development environment around your test run, you
can use models directly in your tests.

Consider a simple models file that includes some doctests:

.. include:: support/pets/models.py
   :literal:

Without NoseGAE, the doctests fail. (To see this we have to run nose
in a new process, since we've already loaded the GAE environment in
this one).

    >>> pets_app = os.path.join(support, 'pets')
    >>> from subprocess import Popen, PIPE
    >>> print Popen(
    ...     ["nosetests", "-v", "--with-doctest", pets_app],
    ...     stderr=PIPE).stderr.read() # doctest: +IGNORE_EXCEPTION_DETAIL +ELLIPSIS +REPORT_NDIFF
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
    Ran 1 test in 0...s
    <BLANKLINE>
    FAILED (errors=1)
    <BLANKLINE>

With NoseGAE, they pass.

    >>> from nose.plugins.doctests import Doctest
    >>> run(argv=['nosetests', '-v', '--with-doctest',
    ...           '--with-gae', '--gae-application', pets_app, pets_app],
    ...     plugins=[Doctest(), NoseGAE()])
    Doctest: models.Pet ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    OK

Realism in testing
~~~~~~~~~~~~~~~~~~

Besides the dev appserver and the datastore, the main sticking point
for testing Google App Engine applications is the highly restrictive
runtime environment. When you test without NoseGAE, tests that should
fail (because the tested code **will fail** when run inside the Google
App Engine) may pass.

For instance, consider an app that writes to a file, like this one:

.. include :: support/badapp/badapp.py

With a simple functional test:

.. include :: support/badapp/test.py

This test will pass when run outside of the Google App Engine environment.

    >>> bad_app = os.path.join(support, 'bad_app')
    >>> print Popen(
    ...     ["nosetests", "-v", bad_app],
    ...     stderr=PIPE).stderr.read() # doctest: +ELLIPSIS +REPORT_NDIFF
    test.test_writing ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    OK
    <BLANKLINE>
    
When run with NoseGAE, it will fail, as it should.

    >>> run(argv=['nosetests', '-v', '--with-gae',
    ...           '--gae-application', bad_app, bad_app],
    ...     plugins=[NoseGAE()])
    test.test_writing ... ERROR
    FIXME

.. _nose : http://somethingaboutorange.com/mrl/projects/nose/
.. _`google app engine` : http://code.google.com/appengine/
.. _wsgi : http://www.wsgi.org/wsgi
