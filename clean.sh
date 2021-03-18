#!/usr/bin/env bash

echo "Cleaning..."

rm -rf -v build/
rm -rf -v dist/
rm -rf -v permedcoe.egg-info/
find permedcoe -type d -iname __pycache__ -delete

echo "----- Cleaning finished -----"
