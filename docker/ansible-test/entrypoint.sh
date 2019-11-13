#!/bin/sh
set -e

# Extract collection to path needed for ansible-test sanity
mkdir -p /ansible_collections/placeholder_namespace/placeholder_name
cd /ansible_collections/placeholder_namespace/placeholder_name

# echo "Downloading collection..."
# curl --insecure --user ansible-insights:redhat https://ci.cloud.redhat.com/api/automation-hub/v3/artifacts/collections/awcrosby.collection_test.1.0.2 -L --output archive.tar.gz
# echo "Extracting collection archive..."
# tar -xzf archive.tar.gz

echo "DEBUG action... Copying/extracting archive instead of downloading..."
cp /google-gcp-1.0.0.tar.gz .
tar -xzf google-gcp-1.0.0.tar.gz

# Rename placeholders in path
NAMESPACE=$(python3 -c "import json; f = open('MANIFEST.json'); namespace = json.load(f)['collection_info']['namespace']; print(namespace); f.close")
NAME=$(python3 -c "import json; f = open('MANIFEST.json'); name = json.load(f)['collection_info']['name']; print(name); f.close")
cd ../../
mv placeholder_namespace/placeholder_name placeholder_namespace/$NAME
mv placeholder_namespace/ $NAMESPACE
cd /ansible_collections/$NAMESPACE/$NAME

echo "Running ansible-test sanity..."
/venv/bin/ansible-test sanity --color

exec "$@"