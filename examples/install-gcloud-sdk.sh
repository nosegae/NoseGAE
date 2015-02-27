#!/bin/bash
cd "$(cd -P -- "$(dirname -- "$0")" && pwd -P)"
if [[ ! -f google-cloud-sdk/path.bash.inc ]]; then
  echo "Downloading google cloud sdk"
  wget https://dl.google.com/dl/cloudsdk/release/google-cloud-sdk.zip
  unzip -qq google-cloud-sdk.zip
  rm google-cloud-sdk.zip
  google-cloud-sdk/install.sh --usage-reporting false --path-update false --rc-path=~/.bashrc --bash-completion false --override-components=app
fi;
google-cloud-sdk/bin/gcloud components update --quiet preview app gae-python
