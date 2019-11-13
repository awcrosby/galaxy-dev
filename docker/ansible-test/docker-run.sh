echo 'Running docker container...'
docker run --rm -it $(docker build -q .)
