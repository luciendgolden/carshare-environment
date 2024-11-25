# G2_generateResponse - Car2Go(Symantic network to text)

## Authors and acknowledgment
- Alexander Watholowitsch 
- Yernar Kumashev 
- Md Rafiqul Islam 
- Mat´uˇs Mrekaj 
- Hoda Kermani

## Description
This is a small part of the Car2Go project. Our main aim is to make RDF data understandable for humans and machines enable two-way communication between self-driving cars and people. The system can answer basic queries about cars, rides, and locations, among other things. Our RDF database is extendable By using an API so that the system can provide more complex answers in future. 

## Project status
Our project can receive text questions as an input through an endpoint, which is then converts to SPARQL using language model. We execute the generated SPARQL query on our GraphDB and receive RDF that has an answer for user's question. Finally, based on the question and resulting rdf from GraphDB, we are generating a human readable text as an answer.
Generation of SAPRQL requires a precise response from the language models. LLaMA model with 7b parameters that is able to run on local machines, fails to provide correct SPARQL queries, therefore, we had to use OpenAI's paid API endpoint for this task. Nevertheless, Llama language module running locally can very well generate human readable answers at the last stage of the GenerateResponse process.


## Project Structure
![Alt text](process.png)

## Visuals
User interface of car2go Web based application.
![Alt text](image.png)

## Installation
- Requirements: 
    - Docker
    - Llama language model
    - Flask (backend)
    - Python
    - VueJs (Frontend)
- Dependencies that have to be installed manually:
    - Llama language model 

### How to run the project(with docker):
- Clone the project: `git clone https://gitlab.dke.univie.ac.at/cmke_ws23/g2_generateresponse.git`
- Download Llama language model form here: `https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/blob/main/mistral-7b-instruct-v0.2.Q3_K_M.gguf`
- Move Llama language model to: `"g2_generateresponse\src\models"`

- Go to directory: `"g2_generateresponse\src"`
- run command: `$ docker-compose up`
- #### Application UI: `http://localhost:8080/` 
- #### Backend API Root: `http://localhost:8000/` 

Alternatively, if your laptop is unable to handle running LLaMA model, you can replace the use of LLaMA with the call to OpenAI. For that, you have to uncomment the LLAMA_ENDPOINT and LLAMA_KEY properties from the docker-compose file. 


## API documentation
port: 8000
### Endpoints:
- **GET** `http://127.0.0.1:8000` (Application root)
- **POST** `/initializeDB` 
  <br/>This endpoint allows you to initialize rdf Graph Database with predefined rdf values. (ALREADY EXECUTED AT THE START UP)
  - Request Body:
    `Content-Type - JSON Content`
    ```text
      {}
    ``` 
  - Response example(200 OK): 
    ```json
    {
      "message": "Repository populated successfully",
      "success": true
    }
    ```
- **POST** `/populateDB` 
  <br/>This endpoint allows you to extend the existing rdf Graph.
  - Request Body:
    `Content-Type - text/plain`
    ```text
      g2:Car1000 rdf:type g2:Car ;
        g2:brand "BMW" ;
        g2:model "G4" ;
        g2:manufactureDate "2023-11-10"^^xsd:date ;
        geo:gpsPosition [
            geo:lat  "47.267815 "^^xsd:float ;
            geo:long "11.393393"^^xsd:float ;
        ] .
    ``` 
  - Response example(200 OK): 
    ```json
    {
      "message": "Repository populated successfully",
      "success": true
    }
    ```
- **POST** `/eraseDB` 
  <br/>This endpoint is for remove all the data from database.
  - Request Body:
    `Content-Type - text/plain`
    ```json
      {}
    ``` 
  - Response example(200 OK): 
    ```json
    {
      "message": "Repository is empty",
      "success": true
    }
    ```

- **POST** `/get-car-list` 
<br/>This endpoint allows you to get all the car list from existing rdf Graph.
  - Request Body:
  `Content-Type - JSON Content`
    ```json
      {}
    ``` 
  - Response example(200 OK): 
    ```json
      {
        "carList": [
          "Car111",
          "Car222",
          "Car333",
          "Car888",
          "Car999"
        ],
        "message": "Car list",
        "success": true
      }
    ```

- **POST** `/question` 
  <br/>This endpoint is used to get questions as a input and process the text to sparrQl query to get the answer from existing rdf Graph Database. In the end It returns the answer of the question.
  - Request Body:
    `Content-Type - JSON Content`
    - senario-1:
    ```json
    {
      "question": "Is the Car222 available?",
      "user_id": "Car222"
    }
    ```
    - senario-2:
    ```json
    {
      "question": "What is the weather in Vienna?",
    }
    ``` 
  - Response example(200 OK): 
    - response-1:
    ```json
    {
      "answer": "Car222 is available."
    }
    ```
    - response-2:
    ```json
    {
      "answer": "The weather in Vienna is rainny.",
    }
    ``` 


## Usage/Usecases
API example:
- **POST** `/question` 
  - Usecase-1(ask car related questions):
    - Request Body:
      `Content-Type - JSON Content`
      ```json
      {
        "question": "Is the Car222 available?",
        "user_id": "Car222"
      }
      ```
    - Response example(200 OK): 
      ```json
      {
        "answer": "The Car222 is available",
      }
      ```
    ---
  - Usecase-2(ask General questions):
    - Request Body:
      `Content-Type - JSON Content`
      ```json
      {
        "question": "What is the recommended action for the weather in Vienna?"
      }
      ```
    - Response example(200 OK): 
      ```json
      {
        "answer": "The weather in Vienna is cloudy, It's recommended to take an Umbrella.",
      }
      ```

## License
Car2Go is licensed under the MIT License.
