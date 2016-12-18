#!/usr/bin/env bash

set -ex

virtualenv env
source env/bin/activate
make bootstrap
make lint
make cover
