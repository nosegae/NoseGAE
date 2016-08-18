#!/bin/bash
mkdir docs
cd docs
pandoc ../README.md -s --highlight-style pygments -o index.html && zip docs.zip index.html
cd -
pandoc README.md -s --highlight-style pygments -o README.rst
