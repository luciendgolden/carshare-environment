# G8_adaptProposal



## List of group members
Alexander Moser, 
Christoph Loik, 
Arthur Rieß, 
Aygun Rzazade,
Noah Weidenhaupt

## How to build

1. Start your local docker engine (make sure you have the latest docker version installed before)
2. run "docker compose up --build" in the g8_adaptproposal/app folder where the docker-compose.yml is located
3. read the Swagger UI for endpoint documentation: http://localhost:8000/apidocs/

## How the project works

1. The model has to be build first by calling the endpoint: http://localhost:8000/train_model
2. After this the predict endpoint can be used by submitting a post request: http://localhost:8000/predict
3. Once predictions have been made the continous learning can be triggered through the retrain_model endpoint under: http://localhost:8000/retrain_model
4. several additional visualization endpoints are document in Swagger UI: http://localhost:8000/apidocs/


The visualization endpoints can also be called directly via the browser after training the model:
### model
http://localhost:8000/visualize_model
### feature importance
http://localhost:8000/visualize_feature_importance
### confusion amtrix
http://localhost:8000/visualize_confusion_matrix

## Adapt the test case

For testing an example is prepared in Swagger UI: http://localhost:8000/apidocs/

The testcase can be adapted freely (however the format of the data should stay the same), the features can take the values described below:
- driving_proficiency = ["Beginner", "Inexperienced", "Intermediate", "Advanced", "Expert", "Professional", "Novice",
                       "Skilled",
                       "Competent"]
- preferred_route_types = ["City", "Highway", "Mixed", "Rural", "Scenic", "Off-road", "Expressway", "Suburban"]
- driving_sickness = ["Yes", "No", "Sometimes", "Rarely", "Occasionally"]
- speed_types = ["Slow", "Moderate", "Fast", "Very Fast", "Leisurely"]
- comfort_importance = ["Low", "Medium", "High", "Extreme"]
- safety_importance = ["Low", "Medium", "High", "Very High", "Top Priority", "Utmost", "Critical"]
- police_records = ["Clean", "Minor Infractions", "Traffic Violations", "Clean Record", "Warnings", "Ticketed",
                  "Misdemeanors"]
- fuel_type_preference = ["Gasoline", "Diesel", "Hybrid", "Electric"]
- transmission_reference = ["Automatic", "Manual"]
- off_road_capability = ["Yes", "No"]
- family_friendly_features = ["Yes", "No"]

## Architecture

The app is based on Flask framework and the packages in the requirements.txt. The major machine learning library used was scikit-learn.
These depencies are automatically installed by docker when a container is started.

