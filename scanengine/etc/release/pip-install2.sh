#!/bin/bash
#
# Copyright (c) nexB Inc. http://www.nexb.com/ - All rights reserved.
#

# ScanEngine release script
# This script creates and tests release archives in the dist/ dir

set -e

# un-comment to trace execution
set -x

echo "###  Installing ScanEngine release with pip ###"

mkdir -p tmp/pip
wget -O tmp/pip/virtualenv.pyz https://bootstrap.pypa.io/virtualenv/2.7/virtualenv.pyz
python2 tmp/pip/virtualenv.pyz tmp/pip
source tmp/pip/bin/activate
pip install dist/scanengine_toolkit*.whl

set +e
set +x
