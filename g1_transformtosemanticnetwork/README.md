# G1_transformToSemanticNetwork

# Semantic Network Transformer

Semantic Network Transformer is a multi-container Docker application designed to convert various open data formats into RDF triples using Apache Jena Fuseki, an in-memory database, and AI services provided by OpenAI's GPT models.

## Components

- `webapp`: A React front-end application for user interactions.
- `server`: A Spring Boot Java application that serves as the backend.
- `database`: An Apache Jena Fuseki server that stores and manages RDF data.

![](uml.png)

## Installation

### Prerequisites

- Docker and Docker Compose installed on your system.
- JDK 17 for compiling the Java application
- Node.js and npm for the web application

### Setting up the application locally

1. run gradle wrapper to build ./gradlew files
2. run ./gradlew build to build the actual jar file
3. run ./gradlew bootRun to run the jar locally

### Setting up the application on docker

Note that the .jar file has to be built under build/libs/g1_transformtosemanticnetwork-1.0.0-release.jar in order to start up the docker container

```
docker-compose up --build -d
```

This will build and start all the necessary Docker containers.

### Configuring OpenAI API Key

To use the AI functionalities, you need to provide your OpenAI API key. The application is configured to read this key from an environment variable. Here's how to set it up:

1. Locate the `docker-compose.yml` file in the root directory of the project.
2. Find the `server` service definition.
3. Replace `key_here` in the `environment` section with your actual OpenAI API key, like so:

```
server:
  ...
  environment:
    - OPENAI_KEY=your_actual_openai_api_key_here
  ...
```
## Usage

After starting the containers and once the application is running, you can:

- Access the web interface at `http://localhost:5173`.
- Interact with the backend server via `http://localhost:8080`.
- Manage the RDF data using the Apache Jena Fuseki dashboard at `http://localhost:3030`.
  (user=admin, password=admin)

You can send requests to the Spring REST Server via the following endpoint:

`localhost:8080/transform`

The data it expects is a POST request with form-data as the body.
The key has to be called `file` and the value a File (`.csv`, `.txt`, etc.) with the car data.
You can use the provided files `NaturalLanguage.txt` or `CARSHARINGGOGD.csv` to test it

## Group Members

Nacewicz Maximilian, Elkaza Saleh, Boroviczeny Philip and Angelov Rumen
