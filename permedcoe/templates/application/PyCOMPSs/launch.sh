#!/usr/bin/env bash

permedcoe execute application app.py --workflow_manager pycompss --flags "-d -g --python_interpreter=python3"

# Using shortcuts:
# permedcoe x app app.py -w pycompss --flags "-d -g --python_interpreter=python3"