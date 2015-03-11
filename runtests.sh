#!/bin/bash
set -e

# run all tests found in examples
for i in $(ls ./examples/*/runtests.sh);
do
    echo "Running test from $(dirname ${i})"
    ${i}
done;