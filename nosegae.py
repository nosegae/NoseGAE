import os
import logging
import sys
import tempfile
from nose.plugins.base import Plugin


log = logging.getLogger(__name__)


class NoseGAE(Plugin):
    """
    Activate this plugin to run tests in Google App Engine dev
    environment. When the plugin is active, Google App Engine dev stubs, such
    as the stub datastore, will be available, and application code will run in
    a sandbox that restricts module loading in the same way as it is
    restricted when running under GAE.
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
        parser.add_option(
            '--without-sandbox', default=True, action='store_false', dest='sandbox_enabled',
            help='Enable this flag if you want to run your tests without '
            'import module sandbox. This is most useful when you have a '
            'conflicting nose plugin (such as coverage).')

    def configure(self, options, config):
        super(NoseGAE, self).configure(options, config)
        if not self.enabled:
            return

        if sys.version_info[0:2] < (2, 7):
            raise EnvironmentError(
                "Python version must be 2.7 or greater, like the Google App Engine environment.  "
                "Tests are running with: %s" % sys.version)

        self._app_path = options.gae_app or config.workingDir
        self._gae_sdk_path = options.gae_lib_root
        if self._gae_sdk_path not in sys.path:
            sys.path.append(self._gae_sdk_path)
        self._data_path = options.gae_data or os.path.join(tempfile.gettempdir(),
                                                           'nosegae.sqlite3')
        self.sandbox_enabled = options.sandbox_enabled

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
        from google.appengine.tools.devappserver2 import application_configuration

        self.configuration = application_configuration.ApplicationConfiguration(
            [self._app_path])
        os.environ['APPLICATION_ID'] = self.configuration.app_id

        # As of SDK 1.2.5 the dev_appserver.py aggressively adds some logging handlers.
        # This removes the handlers but note that Nose will still capture logging and
        # report it during failures.  See Issue 25 for more info.
        rootLogger = logging.getLogger()
        for handler in rootLogger.handlers:
            if isinstance(handler, logging.StreamHandler):
                rootLogger.removeHandler(handler)

    def beforeTest(self, *args):
        from google.appengine.ext import testbed
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # required for queue.yaml so the app knows about the task queue names
        self.testbed.init_taskqueue_stub(root_path=self._app_path)

        # workaround to avoid prospective search complain until there is a proper
        # testbed stub. see http://stackoverflow.com/questions/16026703/testbed-stub-for-google-app-engine-prospective-search
        from google.appengine.api.prospective_search.prospective_search_stub \
            import ProspectiveSearchStub
        PROSPECTIVE_SEARCH_SERVICE_NAME = 'matcher'
        testbed.SUPPORTED_SERVICES.append(PROSPECTIVE_SEARCH_SERVICE_NAME)
        ps_data_file = os.path.join(os.path.split(self._data_path)[0],
                                    'nosegae.ps')
        ps_stub = ProspectiveSearchStub(
            prospective_search_path=ps_data_file,
            taskqueue_stub=self.testbed.get_stub(testbed.TASKQUEUE_SERVICE_NAME))
        self.testbed._register_stub(PROSPECTIVE_SEARCH_SERVICE_NAME, ps_stub)

    def afterTest(self, *args):
        self.testbed.deactivate()
