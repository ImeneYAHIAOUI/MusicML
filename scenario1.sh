#!/bin/bash

echo "Generating Billie jean music..."
cd MusicMl/src
python musicML.py --generate scenarios/BillieJeanDrum.mml

echo "Billie jean music generation completed."
