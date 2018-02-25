#!/bin/bash

rm -rf build
./bin/build_content.py
./bin/build_sitemap.py
./bin/build_index.py
cp -r legacy/css build/
cp -r legacy/images build/
