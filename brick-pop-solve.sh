#!/usr/bin/env bash

set -e

adb devices
adb shell screencap -p | sed 's/\r$//' > brick-pop.png
python src/solve.py brick-pop.png
rm brick-pop.png
