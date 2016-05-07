#!/bin/bash

# Script for zip latest FdiGenerator related files for download
# This script must be called as:
#  scripts/generate_zip_file_for_download.sh

UNAMES="$(uname -s)"

# Check if run this script in the right directory
if [ ! -e fdi_generator.py ]
then
    echo "Run this script in the same folder with fdi_generator.py"
    echo "  Usage: scripts/generate_zip_file_for_download.sh"
    exit
fi

# Import fdi_generator.py to get .pyc bytecode file
echo "Generating .pyc file..."
python -c "import fdi_generator"

# Rename .pyc file to .pyw file
echo "Generating .pyw file..."
mv fdi_generator.pyc FdiGenerator.pyw

mkdir -p FdiGenerator
echo "Copying necessary files to FdiGenerator..."
# Copying file to FdiGenerator folder
cp -rf fdi_generator.py FdiGenerator.pyw library.zip images info output resources test.fdi test.xlsx README.md FdiGenerator

if [[ $UNAMES == 'Linux' ]] || [[ $UNAMES == 'Darwin'  ]]
then
    # Use zip on Linux & Mac OSX
    echo "Zip files on Windows..."
    zip -r FdiGenerator.zip FdiGenerator
elif [[ $UNAMES == CYGWIN* ]] || [[ $UNAMES == MINGW* ]]
then
    # Use zip on Windows
    echo "Zip files..."
    scripts/zip -r FdiGenerator.zip FdiGenerator
else
    echo "Unknown Platform! Zip failed!!"
fi

# Cleaning job
echo "Cleaning ..."
rm -rf FdiGenerator
