import os
import logging
import sys
from warnings import warn
from nose.plugins.base import Plugin


log = logging.getLogger(__name__)


class NoseGAE(Plugin):
    """
    Initialize the GAE environment for a given application at the
    beginning of the test run.
    """
    name = 'gae'
    lib_dirs = ('', 'lib/django', 'lib/webob', 'lib/yaml/lib')
    
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
            'directory (generally the pwd)')

    def configure(self, options, config):
        super(NoseGAE, self).configure(options, config)
        if not self.enabled:
            return
        if options.gae_app is not None:
            self._path = options.gae_app
        else:
            self._path = config.workingDir
        if options.gae_lib_root is not None:
            root = options.gae_lib_root
            for d in self.lib_dirs:
                sys.path.append(os.path.join(root, d))
        try:
            from google.appengine.tools import dev_appserver
            from google.appengine.tools.dev_appserver_main import \
                DEFAULT_ARGS, ARG_CLEAR_DATASTORE, ARG_LOG_LEVEL
            self._gae = {'dev_appserver': dev_appserver,
                         'ARG_LOG_LEVEL': ARG_LOG_LEVEL,
                         'ARG_CLEAR_DATASTORE': ARG_CLEAR_DATASTORE,
                         'DEFAULT_ARGS': DEFAULT_ARGS}
        except ImportError, e:
            self.enabled = False
            warn("Google App Engine not found in %s" % options.gae_lib_root,
                 RuntimeWarning)
                        
    def begin(self):
        gae_opts = self._gae['DEFAULT_ARGS'].copy()
        gae_opts[self._gae['ARG_CLEAR_DATASTORE']] = True
        config, _junk = self._gae['dev_appserver'].LoadAppConfig(self._path, {})
        self._gae['dev_appserver'].SetupStubs(config.application, **gae_opts)
