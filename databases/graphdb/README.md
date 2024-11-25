# GraphDB Database

## Setting up the database on docker

`docker build -t graphdb-image .`

`docker run -p 7200:7200 --name graphdb-container graphdb-image`

## Removing the container

`docker stop graphdb-container && docker rm graphdb-container`