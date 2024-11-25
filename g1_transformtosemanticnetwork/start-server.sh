#!/bin/bash

cd .

# Give execution permissions to the Gradle wrapper
chmod +x ./gradlew

echo "Building the project..."
# Build the project
./gradlew build

# Check if the build was successful
if [ $? -eq 0 ]; then
    echo "Build successful."
else
    echo "Build failed. Exiting..."
    exit 1
fi

echo "Starting the server..."
# Run the project
./gradlew bootRun
