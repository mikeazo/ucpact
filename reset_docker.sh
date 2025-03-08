#!/usr/bin/env bash

set -e

echo -n "Are you sure you want to clear the builder cache and all images/containers? [y/N]: "

read -r resp

if [[ "$resp" == "Y" || "$resp" == "y" ]] ; then echo "Reseting Docker data..." ; else echo "Canceling..." && exit 0 ; fi

if [[ "$(docker ps -a -q)" ]] ; then docker stop $(docker ps -a -q) ; fi

docker container prune -f
docker image prune -a -f
docker builder prune -a -f

echo "Docker was reset successfully!"
