#!/bin/bash
set -e
pip list
$REGRESSION_PATH/main_entry.sh basic
