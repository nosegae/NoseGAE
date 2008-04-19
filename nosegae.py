import os
import pdb
import logging
import sys
from imp import find_module, acquire_lock, release_lock
from warnings import warn
from nose.importer import Importer, add_path
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
        self.config = config
        if options.gae_app is not None:
            self._path = options.gae_app
        else:
            self._path = config.workingDir
        if options.gae_lib_root is not None:
            root = self._gae_path = options.gae_lib_root
            for d in self.lib_dirs:
                sys.path.append(os.path.join(root, d))
        else:
            self._gae_path = None
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
            self._preserve_mods = dict(
                (name, sys.modules[name]) for name in sys.modules.keys()
                if (name.startswith('google')
                    or name.startswith('webob')
                    or name.startswith('yaml')
                    or name.startswith('django')
                    or name.startswith('nose')))
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
        self._install_hook(dev_appserver.HardenedModulesHook)
        # dev_appserver.HardenedModulesHook.ENABLE_LOGGING = True

    def beforeImport(self, filename, module):
        if not self.hook.sandbox:
            if self.hook.should_sandbox(module, filename):
                self.hook.enter_sandbox(module)

    def afterImport(self, filename, module):
        if self.hook.sandbox == module:
            self.hook.exit_sandbox()
                     
    def _install_hook(self, cls):
        dev_appserver = self._gae['dev_appserver']
        class Hook(HookMixin, cls):
            dev_appserver = self._gae['dev_appserver']
            sandbox_root = self._path
            testMatch = self.config.testMatch
            preserve = self._preserve_mods.copy()
        self.hook = Hook(sys.modules)
        sys.meta_path = [self.hook]
        # set up allowed file access paths
        paths = [self._path]
        if self._gae_path:
            paths.append(self._gae_path)
        dev_appserver.FakeFile.SetAllowedPaths(paths)
                                                
        
class HookMixin(object):
    """
    Combine this mixin with a meta_path importer (such as
    dev_appserver.HardenedModulesHook) to set up a meta_path importer that
    enforces the rules of the mixed-in importer only for non-test modules that
    fall under a particular path.

    The subclass defined by mixing this class with an importer must define the
    following attributes:

    * dev_appserver: the google.appengine.tools.dev_appserver module
    * sandbox_root: the path under which non-test modules should be sandboxed
    * testMatch: a regular expression used to distinguish test modules
    """
    sandbox = None
    def find_module(self, fullname, path=None):
        if not self.sandbox:
            if path:
                mod_path = path[0]
            else:
                mod_path = self.find_mod_path(fullname)
            if mod_path and self.should_sandbox(fullname, mod_path):
                self.enter_sandbox(fullname)
        if not self.sandbox:
            # allow normal loading
            self.log("* ALLOW NORMAL LOAD: %s" % fullname)
            return None
        # sandboxed
        return super(HookMixin, self).find_module(fullname, path)
    
    def load_module(self, fullname):
        # only called when sandboxed
        try:
            return super(HookMixin, self).load_module(fullname)
        finally:
            if fullname == self.sandbox:
                self.exit_sandbox()

    def enter_sandbox(self, mod_name):
        if self.sandbox:
            return
        self.log(">>> ENTER sandbox %s" % mod_name)
        self.sandbox = mod_name
        self._old_modules = sys.modules.copy()
        self.dev_appserver.ClearAllButEncodingsModules(sys.modules)
        sys.modules.update(self.preserve)
        if hasattr(sys, 'path_importer_cache'):
            sys.path_importer_cache.clear()
    
    def is_sandboxed(self, mod_name):
        return mod_name == self.sandbox

    def exit_sandbox(self):
        if not self.sandbox:
            return
        self.log("<<< EXIT sandbox %s" % self.sandbox)
        self.sandbox = None
        sys.modules.update(self._old_modules)
        if hasattr(sys, 'path_importer_cache'):
            sys.path_importer_cache.clear()
        
    def find_mod_path(self, fullname):
        # we really only need the path to the top
        top = fullname.split('.')[0]
        try:
            _sf, path, _desc= self._imp.find_module(top, None)
        except ImportError:
            self.log("Could not find path for %s", fullname)
            return
        self.log("Module path for %s is %s", fullname, path)
        return path

    def should_sandbox(self, fullname, mod_path):
        mp = os.path.realpath(mod_path)
        sbp = os.path.realpath(self.sandbox_root)
        self.log("%s under %s?", mp, sbp)
        return mp.startswith(sbp) and not self.testMatch.search(fullname)
