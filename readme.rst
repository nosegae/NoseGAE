---------------------------------------------------
NoseGAE: Test support for Google Application Engine
---------------------------------------------------

    >>> import os
    >>> support = os.path.join(os.path.dirname(os.path.realpath(__file__)),
    ...                        'support')
    >>> hello_app = os.path.join(support, 'helloworld')
    >>> from nose.plugins.plugintest import run
    >>> from nosegae import NoseGAE
    >>> run(argv=['nosegae', '--with-gae', '--gae-application', hello_app, '-v', hello_app], plugins=[NoseGAE()])
    test.test_index ... ok
    <BLANKLINE>
    ----------------------------------------------------------------------
    Ran 1 test in ...s
    <BLANKLINE>
    OK
