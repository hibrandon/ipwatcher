#!/bin/bash

rm -rf build
rm -rf dist
python setupIpWatchdog.py py2app
mv dist/watchIPGui.app ipWatchdog.app

rm -rf build
rm -rf dist
python setupSNS.py py2app
mv dist/emailAfterExec.app SNS.app
