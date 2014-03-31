
import sys
import optparse
import unittest
import mock
from nose.config import Config
from nose.tools import raises
from nosegae import NoseGAE

def mktest():    
    class TC(unittest.TestCase):
        def runTest(self):
            pass
    test = TC()
    return test

mktest.__test__ = False

def test_py_version_too_low():
    
    parser = optparse.OptionParser()
    plugin = NoseGAE()
    plugin.add_options(parser, env={})
    (options, args) = parser.parse_args([
        "--with-gae"
    ])
        
    _version_info = sys.version_info
    sys.version_info = (2, 5, 1, 'final', 0)
    try:
        with mock.patch('sys.exit') as sysexit:
            plugin.configure(options, Config())
            sysexit.assert_called_with(1)
    finally:
        sys.version_info = _version_info

def test_py_version_ok():
    
    parser = optparse.OptionParser()
    plugin = NoseGAE()
    plugin.add_options(parser, env={})
    (options, args) = parser.parse_args([
        "--with-gae"
    ])
        
    _version_info = sys.version_info
    sys.version_info = (2, 7, 0, 'final', 0)
    try:
        plugin.configure(options, Config())
        assert plugin.enabled
    finally:
        sys.version_info = _version_info

    