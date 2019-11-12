echo 'Running docker container...'
docker run --rm -it -v "$(dirname ${PWD})/_collection_on_host:/collection_volume" $(docker build -q .)
