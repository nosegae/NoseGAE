from setuptools import setup

DESCRIPTION = """\
NoseGAE: nose plugin for Google App Engine testing\
"""

LONG_DESCRIPTION = open('docs/readme.html', 'r').read()

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    ("License :: OSI Approved :: GNU Library or "
     "Lesser General Public License (LGPL)"),
    "Topic :: Software Development :: Testing"
    ]
VERSION = '0.1.1'
AUTHOR = 'Jason Pellerin'
AUTHOR_EMAIL = 'jpellerin@gmail.com'

setup(
    name='NoseGAE',
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    url='http://code.google.com/p/nose-gae/',
    license='LGPL License',
    entry_points = {
        'nose.plugins.0.10': [ 'nosegae = nosegae:NoseGAE']
        },
    py_modules = ['nosegae'],
    tests_require = ['WebTest', 'trestle>=0.2a1']
    )
