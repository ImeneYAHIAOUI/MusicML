#!/bin/bash
cd src

echo "Generating BillieJeanDrum with note removal..."
python main.py --generate scenarios/BillieJeanDrum_removeNote.mml

echo "music generation completed."

echo "Generating BillieJeanDrum with note modification..."

python main.py --generate scenarios/BillieJeanDrum_changeNote.mml

echo "music generation completed."
