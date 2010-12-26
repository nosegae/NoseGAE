#!/bin/bash

# See Readme for details on developing NoseGAE...

PY25_ROOT=${PY25_ROOT:=/usr/local/python2.5.5-app-engine}
export PATH=$PY25_ROOT/bin/:${PATH}
nosetests $@
exit $?