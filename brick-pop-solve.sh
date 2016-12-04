#!/usr/bin/env bash

set -e

adb devices
adb shell screencap -p | sed 's/\r$//' > brick-pop.png
python solve.py brick-pop.png
