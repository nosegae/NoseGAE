import __builtin__
import os
import pdb
import logging
import sys
import types
from imp import find_module, acquire_lock, release_lock
from warnings import warn
from nose.importer import Importer, add_path
from nose.plugins.base import Plugin


log = logging.getLogger(__name__)

"""
NOTES

importing is very thorny

what we want is for *test* modules to import normally, but *non-test*
modules to import under the gae restricted environment.

That includes, of course, non-test modules *imported from test modules*

So we need an import hook that turns on gae's restricted environment
only for modules:
 a) under the app path
 c) that don't include 'test' in the name

"""




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
            # prefill these into sys.modules
            import webob
            import yaml
            import django
        except ImportError, e:
            self.enabled = False
            warn("Google App Engine not found in %s" % options.gae_lib_root,
                 RuntimeWarning)
                        
    def begin(self):
        args = self._gae['DEFAULT_ARGS']
        clear = self._gae['ARG_CLEAR_DATASTORE']
        dev_appserver = self._gae['dev_appserver']
        gae_opts = args.copy()
        gae_opts[clear] = True
        config, _junk = dev_appserver.LoadAppConfig(self._path, {})
        dev_appserver.SetupStubs(config.application, **gae_opts)
        dev_appserver.FakeFile.SetAllowedPaths([self._path]) # FIXME
        self._install_hook(dev_appserver.HardenedModulesHook)
        dev_appserver.HardenedModulesHook.ENABLE_LOGGING = True

    def _install_hook(self, cls):
        dev_appserver = self._gae['dev_appserver']
        class Hook(cls):
            depth = 0
            restrict = False
                            
            def find_module(self, fullname, path=None):
                if 'bad_app' in fullname: # FIXME
                    self.restrict = fullname
                    self.log(">>> RESTRICTING")
                    self._old_modules = sys.modules.copy()
                    dev_appserver.ClearAllButEncodingsModules(sys.modules)
                    # FIXME clear path import cache
                    # FIXME possible to patch __builtin__.file, etc?
                if not self.restrict:
                    # allow normal loading
                    self.log("* ALLOW NORMAL LOAD: %s" % fullname)
                    return None
                return cls.find_module(self, fullname, path)

            def load_module(self, fullname):
                try:
                    return cls.load_module(self, fullname)
                finally:
                    if fullname == self.restrict:
                        self.log("<<< END RESTRICT")
                        self.restrict = False
                        sys.modules.update(self._old_modules)
                
        sys.meta_path=[Hook(sys.modules)]
