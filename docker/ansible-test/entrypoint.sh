#!/bin/sh
set -e

# Extract collection to path needed for ansible-test sanity
mkdir -p /ansible_collections/placeholder_namespace/placeholder_name
cd /ansible_collections/placeholder_namespace/placeholder_name

echo "Copying and extracting archive..."
cp /archive/*.tar.gz .
tar -xzf *.tar.gz

# Rename placeholders in path
NAMESPACE=$(python3 -c "import json; f = open('MANIFEST.json'); namespace = json.load(f)['collection_info']['namespace']; print(namespace); f.close")
NAME=$(python3 -c "import json; f = open('MANIFEST.json'); name = json.load(f)['collection_info']['name']; print(name); f.close")
cd ../../
mv placeholder_namespace/placeholder_name placeholder_namespace/$NAME
mv placeholder_namespace/ $NAMESPACE
cd /ansible_collections/$NAMESPACE/$NAME

echo "Running ansible-test sanity..."
/venv/bin/ansible-test sanity --color yes --failure-ok

exec "$@"