#!/bin/bash

echo "Generating Billie jean music..."
cd src
python main.py --generate scenarios/BillieJeanDrum.mml

echo "Billie jean music generation completed."
