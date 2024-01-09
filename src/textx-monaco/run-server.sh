#!/bin/bash

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Informations
PROJECT_DIR="server"
PROJECT_URL="http://127.0.0.1:4000/"

# Se déplacer dans le répertoire "client"
cd "$PROJECT_DIR" || exit

# Afficher un message avec la couleur bleue
echo -e "${BLUE}Changing directory to '$PROJECT_DIR'...${NC}"

echo -e "${BLUE}Executing server.py ...${NC}"

echo -e "${BLUE}Server started ${NC}"
python -W ignore::DeprecationWarning server.py