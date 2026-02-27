#!/bin/bash
# Migrate front matter: remove cn/en from categories, add originalLang
set -euo pipefail

for f in content/post/*/index.md; do
  echo "Processing: $f"

  # Detect language from categories
  if grep -q "^  - cn$" "$f"; then
    LANG="zh"
  elif grep -q "^  - en$" "$f"; then
    LANG="en"
  else
    echo "  SKIP: no cn/en category found"
    continue
  fi

  # Remove the cn/en category line
  if [ "$LANG" = "zh" ]; then
    sed -i '' '/^  - cn$/d' "$f"
  else
    sed -i '' '/^  - en$/d' "$f"
  fi

  # Add originalLang after slug line
  if ! grep -q "^originalLang:" "$f"; then
    sed -i '' "/^slug:/a\\
originalLang: $LANG" "$f"
  fi

  echo "  Done: originalLang=$LANG"
done
