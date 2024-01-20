#!/bin/bash

echo "Generating billie jean drums with regions..."

cd src

./main.py --generate  scenarios/BillieJean_regions.mml

echo "music generation completed."
