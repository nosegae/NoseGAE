from setuptools import setup

DESCRIPTION = """\
NoseGAE: nose plugin for Google App Engine testing\
"""
LONG_DESCRIPTION = """\
Basic usage::
    
    $ cd your/app
    $ nosetests --with-gae

See http://farmdev.com/projects/nosegae/ for complete documentation or open docs/readme.html after downloading the package.

"""
VERSION = '0.1.4'

setup(
    name='NoseGAE',
    version=VERSION,
    author="Jason Pellerin",
    author_email="jpellerin@gmail.com",
    maintainer="Kumar McMillan",
    maintainer_email="kumar.mcmillan@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        ("License :: OSI Approved :: GNU Library or "
         "Lesser General Public License (LGPL)"),
        "Topic :: Software Development :: Testing"
        ],
    url='http://code.google.com/p/nose-gae/',
    license='LGPL License',
    entry_points = {
        'nose.plugins.0.10': [ 'nosegae = nosegae:NoseGAE']
        },
    py_modules = ['nosegae'],
    install_requires = ['nose>=0.10.1'],
    tests_require = ['WebTest', 'trestle>=0.2a1']
    )
