#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <mml_file>"
    exit 1
fi

mml_file=$1

if [ ! -f "scenarios/$mml_file" ]; then
    echo "Error: The specified MML file does not exist in the scenarios directory."
    exit 1
fi

cd src

echo "Generating scenario for $mml_file ..."
python main.py --generate "scenarios/$mml_file" 2>/dev/null

echo "Music generation completed."

