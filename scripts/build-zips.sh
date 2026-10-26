#!/bin/sh
# Builds one zip per skill into dist/ for uploading to claude.ai (Customize › Skills › Upload a skill).
set -e
cd "$(dirname "$0")/.."
rm -rf dist && mkdir dist
cd plugins/local-client-finder/skills
for s in */; do
  s=${s%/}
  zip -qr "../../../dist/$s.zip" "$s" -x '*.DS_Store' '*__pycache__*'
done
cd ../../..
ls -1 dist
