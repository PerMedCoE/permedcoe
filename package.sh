#!/usr/bin/env bash

echo "Packaging..."

python3 -m pip install --upgrade build
python3 -m build

echo "----- Packaging finished -----"
