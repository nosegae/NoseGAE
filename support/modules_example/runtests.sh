#!/bin/bash
# run with ./runtests.sh --gae-lib-root=path/to/google_appengine unless /usr/local/google_appengine
nosetests --with-gae \
          --gae-application='app.yaml,mobile_frontend.yaml,static_backend.yaml,dispatch.yaml' \
          $@