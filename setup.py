from setuptools import setup

DESCRIPTION = "NoseGAE: nose plugin for Google App Engine testing"

VERSION = '0.4.2'

with open('README.md') as file:
    long_description = file.read()

setup(
    name='NoseGAE',
    version=VERSION,
    author="Jason Pellerin",
    author_email="jpellerin@gmail.com",
    maintainer="Josh Johnston",
    maintainer_email="johnston.joshua+nosegae@gmail.com",
    description=DESCRIPTION,
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Testing"
    ],
    url='https://github.com/Trii/NoseGAE',
    download_url='https://github.com/Trii/NoseGAE/tarball/' + VERSION,
    license='BSD License',
    entry_points={
        'nose.plugins.0.10': ['nosegae = nosegae:NoseGAE']
    },
    py_modules=['nosegae'],
    install_requires=['nose>=0.10.1'],
    zip_safe=False
)