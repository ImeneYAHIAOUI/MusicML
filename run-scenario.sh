#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <mml_file>"
    exit 1
fi

mml_file=$1

cd src

echo "Generating scenario for $mml_file ..."
python main.py --generate "scenarios/$mml_file"

echo "Music generation completed."
