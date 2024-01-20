#!/bin/bash

echo "Generating billie jean with sections..."

cd src

./main.py --generate  scenarios/BillieJean_sections.mml

echo "music generation completed."