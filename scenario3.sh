#!/bin/bash

echo "Generating BillieJeanDrum with note removal..."

cd src

./main.py --generate  scenarios/BillieJeanDrum_removeNote.mml

echo "music generation completed."

echo "Generating BillieJeanDrum with note modification..."


./main.py --generate scenarios/BillieJeanDrum_changeNote.mml

echo "music generation completed."
