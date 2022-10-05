#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR=.

GREEN="32"
BOLDGREEN="\e[1;${GREEN}m"
ENDCOLOR="\e[0m"

# Python static code checkers
echo -e "${BOLDGREEN}> running brunette...${ENDCOLOR}"
brunette --check --diff --skip-string-normalization --config setup.cfg "${PROJECT_DIR}"

echo -e "${BOLDGREEN}> running isort...${ENDCOLOR}"
isort --check-only --diff "${PROJECT_DIR}"

echo -e "${BOLDGREEN}> running prospector...${ENDCOLOR}"
prospector "${PROJECT_DIR}"

# Shell static code checkers
echo -e "${BOLDGREEN}> running shellcheck...${ENDCOLOR}"
find "${PROJECT_DIR}" -name "*.sh" -type f -not -path '*/\.venv/*' -exec shellcheck {} \;
