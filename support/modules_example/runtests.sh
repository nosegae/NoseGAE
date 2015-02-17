#!/bin/bash

nosetests --with-gae --gae-lib-root=../../../../google-cloud-sdk/platform/google_appengine \
          --gae-application='app.yaml,mobile_frontend.yaml,static_backend.yaml,dispatch.yaml'