#!/bin/bash

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Informations
PROJECT_DIR="client"
PROJECT_URL="http://127.0.0.1:4000/"

# Se déplacer dans le répertoire "client"
cd "$PROJECT_DIR" || exit

# Afficher un message avec la couleur bleue
echo -e "${BLUE}Changing directory to '$PROJECT_DIR'...${NC}"

# Installer les dépendances du projet avec Yarn
echo -e "${BLUE}Running 'yarn install' to install project dependencies...${NC}"
yarn install

# Démarrer le projet avec Yarn
echo -e "${BLUE}Starting monaco editor with 'yarn start'...${NC}"
yarn start &
wait $!


