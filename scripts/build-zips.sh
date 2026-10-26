#!/bin/sh
# Builds dist/find-clients.zip for uploading to claude.ai (Customize › Skills › Upload a skill).
set -e
cd "$(dirname "$0")/.."
rm -rf dist && mkdir dist
cd plugins/local-client-finder/skills
zip -qr ../../../dist/find-clients.zip find-clients -x '*.DS_Store' '*__pycache__*'
cd ../../..
ls -1 dist
