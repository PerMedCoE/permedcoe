#!/usr/bin/env bash

input_file=$1
output_file=$2
verbose=$3
tmpdir=$4

echo "--------------------------------------------"
echo "Running my_binary.sh"
echo "Parameters:"
echo " - input_file = ${input_file}"
echo " - output_file = ${output_file}"
echo " - verbose = ${verbose}"
echo " - tmpdir = ${tmpdir}"
echo "--------------------------------------------"

CURRENT_DIR=$(pwd)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# Directory where the scripts used by this script are located in the installation folder
SCRIPTS_DIR="${SCRIPT_DIR}/"

# This is the directory where the auxiliary or temporary files will be written and from where the execution will be done
if [ "${tmpdir}" = "pycompss_sandbox" ]; then
    tmpdir=${CURRENT_DIR}
    echo "Using PyCOMPSs sandbox directory as temporary: ${tmpdir}"
else
    echo "Using temporary directory: ${tmpdir}"
    cd ${tmpdir}
fi

# Do whatever is necessary within the asset:
# * It is also possible to write within tmpdir, but requires:
#    - tmpdir has to be added in the task definition
#    - tmpdir has to be enabled in __main__.py
echo "Running..."

cd $CURRENT_DIR
