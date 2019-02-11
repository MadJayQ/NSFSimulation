#!/bin/sh

# Recursively removes all .pyc and __pycache__ folders in the current
# Directory

find . | grep -E "(__pycache__|\.pyc$)" | xargs rm -rf
echo ".pyc and __pycache__ removed. :D"
