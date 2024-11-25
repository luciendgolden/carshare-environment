# Fuseki Database

## Setting up the database on docker

`docker build -t fuseki-image .`

`docker run -p 3030:3030 --name fuseki-container fuseki-image`

## Removing the container

`docker stop fuseki-container && docker rm fuseki-container`