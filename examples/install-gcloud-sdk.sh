#!/bin/bash

cd "$(cd -P -- "$(dirname -- "$0")" && pwd -P)"

if [[ ! -f google-cloud-sdk/path.bash.inc ]]; then
  VERSION=$(echo $(curl 'https://appengine.google.com/api/updatecheck') | \
      sed -E 's/release: \"(.+)\"(.*)/\1/g')
  echo "Downloading App Engine SDK ${VERSION}"
  APP_ENGINE_SDK="google_appengine_${VERSION}.zip"
  wget "https://commondatastorage.googleapis.com/appengine-sdks/featured/${APP_ENGINE_SDK}" -nv
  unzip -q ${APP_ENGINE_SDK} -d .
  echo "Downloading google cloud sdk"
  wget https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.zip
  unzip -qq google-cloud-sdk.zip
  rm google-cloud-sdk.zip
  google-cloud-sdk/install.sh --usage-reporting false --path-update false \
      --rc-path=~/.bashrc --bash-completion false --override-components=app
fi;
google-cloud-sdk/bin/gcloud components update --quiet app
