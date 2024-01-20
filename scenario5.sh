#!/bin/bash

echo "Generating billie jean bass with pitch bend..."

cd src

./main.py --generate  scenarios/BillieJean_pitchbend.mml

echo "music generation completed."
