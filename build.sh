#!/bin/sh
rm -rf build
mkdir -p build
cp *.py build
pipenv lock -r > build/requirements.txt
pip3 install -r build/requirements.txt --no-deps -t build
