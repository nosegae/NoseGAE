#!/bin/bash

if [ "${FD_PROJECTS_HOST}" = "" ]; then
    echo "missing \$FD_PROJECTS_HOST"
    exit 1
fi
if [ "${FD_PROJECTS_PATH_TARGET}" = "" ]; then
    echo "missing \$FD_PROJECTS_PATH_TARGET"
    exit 1
fi
scp ./docs/readme.html ${FD_PROJECTS_HOST}:${FD_PROJECTS_PATH_TARGET}/nosegae/index.html