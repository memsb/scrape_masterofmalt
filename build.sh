#!/bin/sh
rm -rf build
mkdir -p build/src
cp *.py build/src
cp appspec.yml build/src
pipenv lock -r > build/requirements.txt
pip3 install -r build/requirements.txt --no-deps -t build/src
cd build/src
zip -r ../output.zip .
