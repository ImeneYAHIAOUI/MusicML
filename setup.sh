#!/bin/bash

check_installation() {
    package=$1
    if python -c "import $package" 2>/dev/null; then
        echo "$package is already installed."
    else
        echo "$package is not installed. Installing now..."
        pip install $package
    fi
}

packages=("midiutil" "textx" "Flask")

for package in "${packages[@]}"; do
    check_installation $package
done

echo "All installations are complete."
