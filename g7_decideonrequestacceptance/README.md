# Topic 7: Car decides whether a request should be accepted

This project focuses on the implementation of Hidden Markov Models (HMMs).

# Group Members
Wael Alhamzah, Michael Figl, Raphael Kimeswenger, Philipp Saborosch, Mathias Tuschek

## Project Architecture

The project is structured as follows:
- Data Collection and Preprocessing (train_hmm.py): Script for preparing and processing the data.
- Model Training (train_hmm.py): Training the Hidden Markov Model using the processed data.
- Application (autonomous_car.py): Script that utilizes the trained model for cars with different criteria.
- Folder "hmm_experiments" contains various test implementations around hidden markov models using 'hmmlearn'.
- Folder "Group7_Paper" contains Group_7_-_Paper_Hidden_Markov_Models.pdf
- Folder "Presentation" contains Presentation.pdf

## Building and Deploying
- clone this repo
- navigate to root directory of this repo on your machine
- run docker-compose up
- you can now send a HTTP POST request to http://127.0.0.1:5000/api/decide-on-request-acceptance
- (IP might vary on some devices; target IP will be printed to command line anyways)

## Architecture
We train our HMM based on data in "training_data.txt". 
 
For example: 
Customer rating: 5, Predicted demand: high, Weather: sunny

## Tests in Jupyter Notebook
see "test_hmm_model.ipynb"

## Sources and Licenses

Code Sources:
- hmmlearn: Used for implementing Hidden Markov Models. https://github.com/hmmlearn/hmmlearn
- main.py: loosely based on https://www.geeksforgeeks.org/use-jsonify-instead-of-json-dumps-in-flask/
- docker-compose.yml: loosely based on https://docs.docker.com/compose/gettingstarted/ 

# Mapping

customer_mapping = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6:6, 7:7}
pred_demand_mapping = {'high': 0, 'stable': 1, 'low': 2}
weather_mapping = {'rainy': 0, 'cloudy': 1, 'sunny': 2}

# Example

- customer_rating (int): The rating of the customer.
- pred_demand (int): The predicted demand.
- weather (int): The weather condition.

Endpoint: http://localhost:8087/api/decide-on-request-acceptance
HTTP: Post
Body (JSON):
```json
{
    "customer_rating" : 1,
    "pred_demand" : 1,
    "weather" : 1
}
```

## JSONSchema for POST Request

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "customer_rating": {
      "type": "integer",
      "minimum": 0,
      "maximum": 7
    },
    "pred_demand": {
      "type": "integer",
      "minimum": 0,
      "maximum": 2
    },
    "weather": {
      "type": "integer",
      "minimum": 0,
      "maximum": 2
    }
  },
  "required": ["customer_rating", "pred_demand", "weather"],
}
```

