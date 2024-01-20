#!/bin/bash


for scenario in scenarios/*.mml
do
    ./run-scenario.sh $(basename $scenario) &
done