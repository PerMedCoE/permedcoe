#!/usr/bin/env bash

in_file=$1
out_file=$2

permedcoe execute application app.py ${in_file} ${out_file}

# Using shortcuts:
# permedcoe x app app.py ${in_file} ${out_file}
