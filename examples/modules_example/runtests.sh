#!/bin/bash
cd "$(cd -P -- "$(dirname -- "$0")" && pwd -P)"
nosetests --with-gae --gae-lib-root ${GAE_PYTHONPATH} \
          --gae-application='app.yaml,mobile_frontend.yaml,static_backend.yaml,dispatch.yaml'
