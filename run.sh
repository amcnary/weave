#!/bin/sh

# Root directory for the server as the first arg, or current path by default.
ROOT_DIR=${1-.}
# Port to use for server, or 8000 by default.
PORT=${2-8000}
# Convenience tag for docker reference.
TAG=directory_app:latest

# Build the Docker image
docker build -t $TAG .

# Run the docker image, passing the port and root directory into the
# python script.
docker run -d -p $PORT:$PORT $TAG $ROOT_DIR $PORT

echo Listening at 127.0.0.1:$PORT