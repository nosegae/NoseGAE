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

# import ihooks

# class MyModuleLoader(ihooks.ModuleLoader):

#     def load_module(self, name, stuff):
#         print "Loading %s (%s)" % (name, stuff)
#         return ihooks.ModuleLoader.load_module(self, name, stuff)
# ihooks.ModuleImporter(MyModuleLoader()).install()

#def c(path):
#    print "Called for %s" % path
#    raise ImportError("whatever")
#sys.path_hooks.append(c)



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
        #self._hook = dev_appserver.HardenedModulesHook(sys.modules)
        self._install_hook(dev_appserver.HardenedModulesHook)
        dev_appserver.HardenedModulesHook.ENABLE_LOGGING = True

    def _install_hook(self, cls):
        dev_appserver = self._gae['dev_appserver']
        class Hook(cls):
            depth = 0
            restrict = False
                            
            def find_module(self, fullname, path=None):
                self.depth += 1
#                 print "%s Find module! %s, %s (%s)" % (
#                     ' ' * self.depth, fullname, path, self.restrict)
                submodule = fullname.split('.')[-1]
                if 'bad_app' in fullname:
                    self.restrict = True
                if self.restrict:
                    old_modules = sys.modules.copy()
                    # FIXME really preserve some, but which?
                    dev_appserver.ClearAllButEncodingsModules(sys.modules)
                    try:
                        source_file, pathname, description = \
                                  self.FindModuleRestricted(
                            submodule, fullname, path)
                    finally:
                        sys.modules.update(old_modules)
#                 try:
#                     source_file, pathname, description = \
#                                  self.FindModuleRestricted(
#                         submodule, fullname, path)
#                     # print "found?", source_file, pathname, description
#                     # If path is under my app path
#                     # and the name doesn't match test match
#                     # enter restricted mode
#                 except ImportError, e:
#                     print "%s ooh, got %s" % (' ' * self.depth, e)
#                     # raise if restricted
                return cls.find_module(self, fullname, path)

            def load_module(self, fullname):
#                 print "%s Load module! %s (%s)" % (' ' * self.depth, fullname, self.restrict)
                if self.restrict:
                    old_modules = sys.modules.copy()
                    dev_appserver.ClearAllButEncodingsModules(sys.modules)
                try:
                    mod = cls.load_module(self, fullname)
                finally:
                    if self.restrict:
                        sys.modules.update(old_modules)
                if self.restrict and 'bad_app' in fullname:
                    self.restrict = False
                    print "%s Ending restricions (%s)" % (' ' * self.depth, mod)
                self.depth -= 1
                if self.depth < 0:
                    print "*** < 0"
                    self.depth = 0
                return mod

                
        sys.meta_path=[Hook(sys.modules)]
        
#    def prepareTestLoader(self, loader):
#        loader.importer = GAEImporter(loader.config,
#                                      self._gae['dev_appserver'],
#                                      self._hook)
    
#     def beforeContext(self):
#         print "Before context"
#         self._metapath = sys.meta_path[:]
#         sys.meta_path = [self._hook]
#         if hasattr(sys, 'path_importer_cache'):
#              self._path_importer_cache = sys.path_importer_cache.copy()
#              sys.path_importer_cache.clear()

#     def afterContext(self):
#         print "After context"
#         sys.meta_path = self._metapath[:]
#         if hasattr(sys, 'path_importer_cache'):
#             sys.path_importer_cache = self._path_importer_cache.copy()

#     def beforeContext(self):
#         # install restricted gae modules
#         # print "before test is ", test
#         dev_appserver = self._gae['dev_appserver']
#         self._modules = sys.modules.copy()
#         self._metapath = sys.meta_path[:]
#         if hasattr(sys, 'path_importer_cache'):
#             self._path_importer_cache = sys.path_importer_cache.copy()
#         self._builtin = __builtin__.__dict__.copy()
#         self._filetype = types.FileType
#         self._clear_modules(sys.modules)
#         sys.meta_path = [dev_appserver.HardenedModulesHook(sys.modules)]
#         if hasattr(sys, 'path_importer_cache'):
#             sys.path_importer_cache.clear()
#         #__builtin__.file = dev_appserver.FakeFile
#         #__builtin__.open = dev_appserver.FakeFile
#         types.FileType = dev_appserver.FakeFile
#         #print "after before test is", test

#     def addError(self, test, err):
#         print "addError '%r' '%r'" % (err, test)
#         #pdb.set_trace()

#     def afterContext(self):
#         # restore real modules
#         #print "before after test is", test
#         dev_appserver = self._gae['dev_appserver']
#         self._modules.update(sys.modules)
#         self._clear_modules(sys.modules)
#         sys.modules.update(self._modules)
#         sys.meta_path = self._metapath[:]
#         if hasattr(sys, 'path_importer_cache'):
#             sys.path_importer_cache = self._path_importer_cache.copy()
#         __builtin__.__dict__.update(self._builtin)
#         types.FileType = self._filetype
#         #print "after after test is", test

#     def _clear_modules(self, mod_dict):
#         enc = self._gae['dev_appserver'].IsEncodingsModule
#         nose = lambda n: n.startswith('nose')
#         for name in mod_dict.keys():
#             if not enc(name) and not nose(name):
#                 del mod_dict[name]


class GAEImporter(Importer):
    def __init__(self, config, dev_appserver, hook):
        self.config = config
        self.dev_appserver = dev_appserver
        self.hook = hook

    def importFromDir(self, dir, fqname):
        """Import a module *only* from path, ignoring sys.path and
        reloading if the version in sys.modules is not the one we want.
        """
        hook = self.hook
        dev_appserver = self.dev_appserver
        dir = os.path.normpath(os.path.abspath(dir))
        log.debug("Import %s from %s", fqname, dir)

        # FIXME reimplement local per-dir cache?
        
        # special case for __main__
        if fqname == '__main__':
            return sys.modules[fqname]
        
        if self.config.addPaths:
            add_path(dir, self.config)

        old_module_dict = sys.modules.copy()
        old_builtin = __builtin__.__dict__.copy()
        #old_argv = sys.argv
        #old_stdin = sys.stdin
        #old_stdout = sys.stdout
        #old_env = os.environ.copy()
        #old_cwd = os.getcwd()
        old_file_type = types.FileType
        reset_modules = False
        
        dev_appserver.ClearAllButEncodingsModules(sys.modules)
        #sys.modules.update(module_dict)
        sys.meta_path = [hook]
        if hasattr(sys, 'path_importer_cache'):
            sys.path_importer_cache.clear()
        __builtin__.file = dev_appserver.FakeFile
        __builtin__.open = dev_appserver.FakeFile
        types.FileType = dev_appserver.FakeFile
        __builtin__.buffer = dev_appserver.NotImplementedFake
        
        try:
            path = [dir]
            parts = fqname.split('.')
            part = parts[-1]
            print "Loading %s from %s (%s)" % (part, fqname, path)
            return hook.FindAndLoadModule(part, fqname, path)
        finally:
            sys.meta_path = []
            sys.path_importer_cache.clear()
            sys.modules.update(old_module_dict)
            __builtin__.__dict__.update(old_builtin)
        
