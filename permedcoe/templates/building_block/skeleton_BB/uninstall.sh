#!/usr/bin/env bash

echo "Uninstalling..."

# python3 -m pip uninstall NEW_NAME

xargs rm -rf < installed_files.txt

rm installed_files.txt

echo "----- Uninstall finished -----"