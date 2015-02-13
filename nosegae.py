import os
import logging
import sys
import tempfile
from nose.plugins.base import Plugin
from nose.case import FunctionTestCase

# Solution from
# http://stackoverflow.com/questions/17583443/what-is-the-correct-way-to-share-package-version-with-setup-py-and-the-package
from pkg_resources import get_distribution, DistributionNotFound

try:
    _dist = get_distribution('nosegae')
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, 'nosegae')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'DEVELOPMENT'
else:
    __version__ = _dist.version

logger = logging.getLogger(__name__)


class NoseGAE(Plugin):
    """Activate this plugin to run tests in Google App Engine dev environment. When the plugin is active,
    Google App Engine dev stubs such as the datastore, memcache, taskqueue, and more can be made available.
    """
    name = 'gae'

    def options(self, parser, env=os.environ):
        super(NoseGAE, self).options(parser, env)
        parser.add_option(
            '--gae-lib-root', default='/usr/local/google_appengine',
            dest='gae_lib_root',
            help='Set the path to the root directory of the Google '
            'Application Engine installation')
        parser.add_option(
            '--gae-application', default=None, action='store', dest='gae_app',
            help='Set the path to the GAE application '
            'under test. Default is the nose `where` '
            'directory (generally the cwd)')
        parser.add_option(
            '--gae-datastore', default=None, action='store', dest='gae_data',
            help='Set the path to the GAE datastore to use in tests. '
            'Note that when using an existing datastore directory, the '
            'datastore will not be cleared before testing begins.')

    def configure(self, options, config):
        super(NoseGAE, self).configure(options, config)
        if not self.enabled:
            return

        if sys.version_info[0:2] < (2, 7):
            raise EnvironmentError(
                "Python version must be 2.7 or greater, like the Google App Engine environment.  "
                "Tests are running with: %s" % sys.version)

        if options.gae_lib_root not in sys.path:
            sys.path.append(options.gae_lib_root)

        self._app_path = options.gae_app or config.workingDir
        self._data_path = options.gae_data or os.path.join(tempfile.gettempdir(),
                                                           'nosegae.sqlite3')

        if 'google' in sys.modules:
            # make sure an egg (e.g. protobuf) is not cached
            # with the wrong path:
            del sys.modules['google']
        try:
            import appengine_config
        except ImportError:
            pass

        import dev_appserver
        dev_appserver.fix_sys_path()  # add paths to libs specified in app.yaml, etc

        # This file handles some OS compat settings. Most notably the `TZ` stuff
        # to resolve https://github.com/Trii/NoseGAE/issues/14.
        # It may need to be removed in the future if Google changes the functionality
        import google.appengine.tools.os_compat

        from google.appengine.tools.devappserver2 import application_configuration

        # get the app id out of your app.yaml and stuff
        configuration = application_configuration.ApplicationConfiguration([self._app_path])

        os.environ['APPLICATION_ID'] = configuration.app_id
        # simulate same environment as devappserver2
        os.environ['CURRENT_VERSION_ID'] = configuration.modules[0].version_id

        self.is_doctests = options.enable_plugin_doctest

    def startTest(self, test):
        """Initializes Testbed stubs based off of attributes of the executing test

        allow tests to register and configure stubs by setting properties like
        nosegae_<stub_name> and nosegae_<stub_name>_kwargs

        Example

        class MyTest(unittest.TestCase):
            nosegae_datastore_v3 = True
            nosegae_datastore_v3_kwargs = {
              'datastore_file': '/tmp/nosegae.sqlite3,
              'use_sqlite': True
            }

            def test_something(self):
               entity = MyModel(name='NoseGAE')
               entity.put()
               self.assertNotNone(entity.key.id())

        Args
            :param test: The unittest.TestCase being run
            :type test: unittest.TestCase
        """
        from google.appengine.ext import testbed

        self._add_missing_stubs(testbed)

        self.testbed = testbed.Testbed()
        self.testbed.activate()
        # Give the test access to the active testbed
        the_test = test.test
        if isinstance(the_test, FunctionTestCase):
            the_test = the_test.test
        the_test.testbed = self.testbed

        for stub_name, stub_init in testbed.INIT_STUB_METHOD_NAMES.iteritems():
            if not getattr(the_test, 'nosegae_%s' % stub_name, False):
                continue
            stub_kwargs = getattr(the_test, 'nosegae_%s_kwargs' % stub_name, {})
            if stub_name == testbed.TASKQUEUE_SERVICE_NAME:
                # root_path is required so the stub can find queue.yaml
                task_args = dict(root_path=self._app_path)
                task_args.update(stub_kwargs)
                stub_kwargs = task_args
            elif stub_name == testbed.DATASTORE_SERVICE_NAME:
                if not self.testbed.get_stub(testbed.MEMCACHE_SERVICE_NAME):
                    # ndb requires memcache so enable it as well as the datastore_v3
                    self.testbed.init_memcache_stub()
                task_args = dict(datastore_file=self._data_path)
                task_args.update(stub_kwargs)
                stub_kwargs = task_args
            elif stub_name == testbed.USER_SERVICE_NAME:
                self.testbed.setup_env(overwrite=True,
                                       USER_ID=stub_kwargs.pop('USER_ID', 'testuser'),
                                       USER_EMAIL=stub_kwargs.pop('USER_EMAIL', 'testuser@example.org'),
                                       USER_IS_ADMIN=stub_kwargs.pop('USER_IS_ADMIN', '1'))
            getattr(self.testbed, stub_init)(**stub_kwargs)

        if self.is_doctests:
            self._doctest_compat(the_test)
        self.the_test = the_test

    def stopTest(self, test):
        self.testbed.deactivate()
        del self.the_test.testbed
        del self.the_test

    def _doctest_compat(self, the_test):
        """Enable compatibility with doctests by setting the current testbed into the doctest scope"""
        try:
            the_test._dt_test.globs['testbed'] = self.testbed
        except AttributeError:
            # not a nose.plugins.doctests.DocTestCase?
            pass

    def _add_missing_stubs(self, testbed):
        """Monkeypatch the testbed for stubs that do not have an init method yet"""
        if not hasattr(testbed, 'PROSPECTIVE_SEARCH_SERVICE_NAME'):
            from google.appengine.api.prospective_search.prospective_search_stub import ProspectiveSearchStub
            testbed.PROSPECTIVE_SEARCH_SERVICE_NAME = 'matcher'
            testbed.INIT_STUB_METHOD_NAMES.update({
                testbed.PROSPECTIVE_SEARCH_SERVICE_NAME: 'init_prospective_search_stub'
            })

            def init_prospective_search_stub(self, enable=True, data_file=None):
                """Workaround to avoid prospective search complain until there is a proper testbed stub

                http://stackoverflow.com/questions/16026703/testbed-stub-for-google-app-engine-prospective-search

                Args:
                    :param self: The Testbed instance.
                    :param enable: True if the fake service should be enabled, False if real
                        service should be disabled.
                """

                if not enable:
                    self._disable_stub(testbed.PROSPECTIVE_SEARCH_SERVICE_NAME)
                    return
                stub = ProspectiveSearchStub(
                    prospective_search_path=data_file,
                    taskqueue_stub=self.get_stub(testbed.TASKQUEUE_SERVICE_NAME))
                self._register_stub(testbed.PROSPECTIVE_SEARCH_SERVICE_NAME, stub)
            testbed.Testbed.init_prospective_search_stub = init_prospective_search_stub
