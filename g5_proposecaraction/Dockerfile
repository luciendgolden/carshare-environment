# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y python3 && \
    python3 -m pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV FLASK_APP=rest.py

# Make port 8085 available to the world outside this container
EXPOSE 8085

# Define the command to run the application
ENTRYPOINT ["flask"]
CMD ["run", "--host", "0.0.0.0", "--port", "8085"]