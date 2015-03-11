#!/bin/bash
cd "$(cd -P -- "$(dirname -- "$0")" && pwd -P)"
nosetests --with-gae --gae-lib-root ../google-cloud-sdk/platform/google_appengine \
          --gae-application='default/app.yaml,mobile/mobile_frontend.yaml,static/static_backend.yaml,dispatch.yaml'
