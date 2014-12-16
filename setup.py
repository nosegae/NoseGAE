from setuptools import setup

DESCRIPTION = """\
NoseGAE: nose plugin for Google App Engine testing\
"""
LONG_DESCRIPTION = """\
Basic usage::
    
    $ cd your/app
    $ nosetests --with-gae

See http://farmdev.com/projects/nosegae/ for complete documentation
or open docs/readme.html after downloading the package.

"""
VERSION = '0.4.0.dev0'

setup(
    name='NoseGAE',
    version=VERSION,
    author="Jason Pellerin",
    author_email="jpellerin@gmail.com",
    maintainer="Josh Johnston",
    maintainer_email="johnston.joshua+nosegae@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Topic :: Software Development :: Testing"
        ],
    url='https://github.com/Trii/NoseGAE',
    license='LGPL License',
    entry_points={
        'nose.plugins.0.10': ['nosegae = nosegae:NoseGAE']
        },
    py_modules=['nosegae'],
    install_requires=['nose>=1.0'],
    # tests_require=['WebTest', 'trestle>=0.2a1', 'Mock']
    )
