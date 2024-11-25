"""Flask App exposing the endpoints for the adaptProposal decision tree"""
from flask import Flask, request, jsonify, render_template
from flasgger import Swagger, swag_from
import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')

from adapt_proposal_model import AdaptProposalModel

app = Flask(__name__)

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Adapt Proposal",
        "description": "API Documentation for the adapt proposal model",
        "contact": {
            "name": "Admin",
            "url": "https://gitlab.dke.univie.ac.at/cmke_ws23/g8_adaptproposal",
        },
        "version": "1.0",
        "basePath": "http://localhost:8000",
    },
    "schemes": [
        "http",
        "https"
    ],
}

swagger_config = {
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST"),
    ],
    "specs": [
        {
            "endpoint": 'Adapt_Proposal',
            "route": '/Adapt_Proposal.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",

}
swagger = Swagger(app, template=swagger_template, config=swagger_config)

app.trained_model = None
app.label_encoders = None
app.accumulated_data = []

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
data_path = os.path.join(BASE_DIR, "sample_data", "generated_drivers.json")

def pretrain_model():
    """
    Pretrains the model with sample data.
    """
    try:
        data = pd.read_json(data_path)
        app.trained_model, app.label_encoders = AdaptProposalModel.train_model(data)
        print("Model pretrained successfully.")
    except Exception as e:
        print(f"Error during model pretraining: {e}")

pretrain_model()

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'g8_adaptproposal API',
        'success': True,
        'endpoints': [
            '/ping',
            '/train_model',
            '/predict',
            '/retrain_model',
            '/visualize_model',
            '/visualize_feature_importance',
            '/visualize_confusion_matrix'
        ],
        'swagger_docs': '/apidocs/'
    })

@swag_from("docs/ping.yaml" )
@app.route('/ping', methods=['GET'])
def ping():
    """
    # ping for testing if endpoints work
    :return: json
    """
    try:
        return jsonify({'message': 'Ping successful'})

    except Exception as e:
        app.logger.error("Error processing request: %s", e)
        return jsonify({'error': str(e)}), 500


@swag_from("docs/train_model.yaml" )
@app.route('/train_model', methods=['GET'])
def train_model_endpoint():
    """
    Train model using generated_drivers.json
    :return: json
    """
    try:

        data = pd.read_json(data_path)

        app.trained_model, app.label_encoders = AdaptProposalModel.train_model(data)

        return jsonify({'message': 'Model trained successfully'})

    except Exception as e:
        app.logger.error("Error processing request: %s", e)
        return jsonify({'error': str(e)}), 500


@swag_from("docs/predict.yaml" )
@app.route('/predict', methods=['POST'])
def predict_endpoint():
    """
    Predict cars for posted preferences
    :return: top cars fitting the preferences
    """
    try:
        new_driver_data = request.get_json()

        predicted_car, top3_cars, prediction_probabilities = AdaptProposalModel.predict(app.trained_model,
                                                                                        app.label_encoders,
                                                                                        new_driver_data)

        # Add the predicted car to accumulated data
        new_driver_data['car'] = predicted_car
        app.accumulated_data.append(new_driver_data)

        return jsonify({
            'predicted_car': predicted_car,
            'top3_cars': top3_cars,
            'prediction_probabilities': prediction_probabilities
        })

    except Exception as e:
        app.logger.error("Error processing request: %s", e)
        return jsonify({'error': str(e)}), 500


@swag_from("docs/retrain_model.yaml" )
@app.route('/retrain_model', methods=['GET'])
def retrain_model_endpoint():
    """
    # Retrain the model using the generated_drivers.json and the accumulated data
    :return: json
    """
    try:
        if not app.accumulated_data:
            return jsonify({'message': 'No new data for retraining'})

        data = pd.read_json(data_path)

        app.trained_model, app.label_encoders = AdaptProposalModel.retrain_model(data, app.accumulated_data)

        app.accumulated_data = []

        return jsonify({'message': 'Model retrained successfully'})

    except Exception as e:
        app.logger.error("Error processing request: %s", e)
        return jsonify({'error': str(e)}), 500


@swag_from("docs/visualize_model.yaml" )
@app.route('/visualize_model', methods=['GET'])
def visualize_model_endpoint():
    """
    endpoint to visualize the trained model
    :return:
    """
    try:

        # Load data from the JSON file and extract the names of the features
        data = pd.read_json(data_path)

        img_data = AdaptProposalModel.visualize_nth_tree(app.trained_model, data, 15)  # 1 ... 100

        return render_template('index.html', img_data=img_data)

    except Exception as e:
        app.logger.error("Error processing request: %s", e)
        return jsonify({'error': str(e)}), 500


@swag_from("docs/visualize_feature_importance.yaml" )
@app.route('/visualize_feature_importance', methods=['GET'])
def visualize_feature_importance_endpoint():
    """
    endpoint to visualize feature importance
    :return:
    """
    try:

        # Load data from the JSON file
        data = pd.read_json(data_path)

        img_data = AdaptProposalModel.visualize_feature_importance(app.trained_model, data)

        return render_template('index.html', img_data=img_data)

    except Exception as e:
        app.logger.error("Error processing request: %s", e)
        return jsonify({'error': str(e)}), 500


@swag_from("docs/visualize_confusion_matrix.yaml")
@app.route('/visualize_confusion_matrix', methods=['GET'])
def visualize_confusion_matrix_endpoint():
    """
    endpoint to visualize confusion matrix
    :return:
    """
    try:

        # Load data from the JSON file and extract the names of the features
        data = pd.read_json(data_path)

        img_data = AdaptProposalModel.visualize_confusion_matrix(app.trained_model, data)

        return render_template('index.html', img_data=img_data)

    except Exception as e:
        app.logger.error("Error processing request: %s", e)
        return jsonify({'error': str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8088)
