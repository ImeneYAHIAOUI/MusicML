#!/bin/bash

echo "Generating BillieJeanDrum with note removal..."

./generate.sh  scenarios/BillieJeanDrum_removeNote.mml

echo "music generation completed."

echo "Generating BillieJeanDrum with note modification..."

./generate.sh  scenarios/BillieJeanDrum_changeNote.mml

echo "music generation completed."
