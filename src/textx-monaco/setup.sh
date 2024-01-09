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

check_yarn() {
    if command -v yarn &> /dev/null; then
        echo "yarn is already installed."
    else
        echo "yarn is not installed. Installing now..."
        npm install -g yarn
    fi
}


packages=("pygls" "lsprotocol" "textx")

for package in "${packages[@]}"; do
    check_installation $package
done

check_yarn

echo "All installations are complete."