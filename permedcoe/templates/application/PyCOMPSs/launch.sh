#!/usr/bin/env bash

in_file=$1
out_file=$2

permedcoe execute application app.py  ${in_file} ${out_file} --workflow_manager pycompss --flags "-d -g --python_interpreter=python3"

# Using shortcuts:
# permedcoe x app app.py  ${in_file} ${out_file} -w pycompss --flags "-d -g --python_interpreter=python3"
