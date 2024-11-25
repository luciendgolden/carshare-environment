#!/bin/bash

IMAGE_NAME="fuseki-image"
CONTAINER_NAME="fuseki-container"

if [ $(docker ps -q -f name=^/${CONTAINER_NAME}$) ]; then
    echo "Container ${CONTAINER_NAME} is already running."
    exit 1
fi

if [ $(docker ps -aq -f name=^/${CONTAINER_NAME}$) ]; then
    echo "Removing existing container ${CONTAINER_NAME}..."
    docker rm ${CONTAINER_NAME}
fi

echo "Building Docker image ${IMAGE_NAME}..."
docker build -t ${IMAGE_NAME} .

if [ $? -eq 0 ]; then
    echo "Docker image ${IMAGE_NAME} built successfully."
else
    echo "Failed to build Docker image ${IMAGE_NAME}."
    exit 1
fi

echo "Starting container ${CONTAINER_NAME} from image ${IMAGE_NAME}..."
docker run -p 3030:3030 --name ${CONTAINER_NAME} ${IMAGE_NAME}

if [ $? -eq 0 ]; then
    echo "Container ${CONTAINER_NAME} started successfully."
else
    echo "Failed to start container ${CONTAINER_NAME}."
    exit 1
fi
