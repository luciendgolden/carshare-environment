from flask import Flask, request, jsonify
import numpy as np
from autonomous_car import AutonomousCar
from train_hmm import train_hmm_models

models, columns = train_hmm_models('training_data.txt')
pos_customer = models[0].predict([[0], [5]])[-1]
pos_pred = models[1].predict([[0], [2]])[-1]
pos_weather = models[2].predict([[0], [2]])[-1]

car = AutonomousCar(0.5, 0.3, 0.2, 0.5)

def makeDecision(customer_rating: int, pred_demand: int, weather: int) -> bool:
    arr = [0, customer_rating]
    arr2 = [0, pred_demand]
    arr3 = [0, weather]
    arr = np.array(arr).reshape(-1, 1)
    arr2 = np.array(arr2).reshape(-1, 1)
    arr3 = np.array(arr3).reshape(-1, 1)
    prediction_customer_rating = models[0].predict(arr)[-1]
    print(prediction_customer_rating)
    prediction_pred_demand = models[1].predict(arr2)[-1]
    prediction_weather = models[2].predict(arr3)[-1]
    result = car.should_accept_ride(prediction_customer_rating, prediction_pred_demand, prediction_weather)
    print(result)
    

    return result

# define Rest API
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'g7_decideonrequestacceptance', 'success': True })

@app.route('/decide-on-request-acceptance', methods=['POST'])
def decideOnRequestAcceptance():
    try:
        request_data = request.get_json()
        customer_rating = request_data['customer_rating']
        pred_demand = request_data['pred_demand']
        weather = request_data['weather']
        decision = {'decision': bool(makeDecision(customer_rating, pred_demand, weather))}
        print(decision)
        return jsonify(decision)
    except Exception as request_exception:
        return jsonify({'error': {request_exception}}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

