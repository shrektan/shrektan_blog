#!/bin/bash
# Usage: ./scripts/translate.sh content/post/2025-05-05-slug/
# Generates the missing language version of a post.
set -euo pipefail

POST_DIR="${1:?Usage: $0 <post-directory>}"

if [ ! -d "$POST_DIR" ]; then
  echo "Error: Directory $POST_DIR does not exist"
  exit 1
fi

ZH_FILE="$POST_DIR/index.md"
EN_FILE="$POST_DIR/index.en.md"

if [ -f "$ZH_FILE" ] && [ ! -f "$EN_FILE" ]; then
  echo "Chinese source found. Will generate English version."
  echo "Source: $ZH_FILE"
  echo "Target: $EN_FILE"
  echo ""
  echo "TODO: Integrate with AI translation API"
  echo "For now, copy and manually translate:"
  cp "$ZH_FILE" "$EN_FILE"
  echo "Created: $EN_FILE (copy of Chinese — please translate)"

elif [ -f "$EN_FILE" ] && [ ! -f "$ZH_FILE" ]; then
  echo "English source found. Will generate Chinese version."
  echo "Source: $EN_FILE"
  echo "Target: $ZH_FILE"
  echo ""
  cp "$EN_FILE" "$ZH_FILE"
  echo "Created: $ZH_FILE (copy of English — please translate)"

elif [ -f "$ZH_FILE" ] && [ -f "$EN_FILE" ]; then
  echo "Both versions already exist:"
  echo "  $ZH_FILE"
  echo "  $EN_FILE"
  exit 0

else
  echo "Error: No index.md or index.en.md found in $POST_DIR"
  exit 1
fi
