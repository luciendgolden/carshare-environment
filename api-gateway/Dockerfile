FROM node:16-alpine

WORKDIR /app

# Copy package.json
COPY package*.json ./
RUN npm install

# Copy all the source code
COPY . .

# Expose port 8080
EXPOSE 8080

# Start the application using the correct entry point
CMD ["node", "./bin/www.js"]
