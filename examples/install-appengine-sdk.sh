#!/bin/bash

cd "$(cd -P -- "$(dirname -- "$0")" && pwd -P)"

VERSION=$(echo $(curl 'https://appengine.google.com/api/updatecheck') | \
  sed -E 's/release: \"(.+)\"(.*)/\1/g')
echo "Downloading App Engine SDK ${VERSION}"
APP_ENGINE_SDK="google_appengine_${VERSION}.zip"
wget "https://commondatastorage.googleapis.com/appengine-sdks/featured/${APP_ENGINE_SDK}" -nv
unzip -q ${APP_ENGINE_SDK} -d .
rm ${APP_ENGINE_SDK}
