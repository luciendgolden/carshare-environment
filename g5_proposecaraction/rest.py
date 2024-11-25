from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from utils.validators import validate_car_state
from utils.helpers import time_to_decimal
from main import determine_actions

app = Flask(__name__)

SWAGGER_URL = '/apidocs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Fuzzy Logic Application"
    },
)

app.register_blueprint(swaggerui_blueprint)

@app.route("/", methods=['GET'])
def home():
    return jsonify({
        "message": "G5 Propose Car Action",
        "success": True
    })

@app.route("/test", methods=['GET'])
def index():
    return jsonify({"greeting":"hey"})

@app.route("/car-actions", methods=['POST'])
def car_actions():
    data = request.get_json()

    if not validate_car_state(data):
        return jsonify({"message": "Invalid input"}), 400
    
    if 'daytime' in data:
        try:
            data['daytime'] = time_to_decimal(data['daytime'])
        except ValueError as e:
            return jsonify({"message": str(e)}), 400

    actions = determine_actions(data)

    return jsonify(actions)

if __name__ == '__main__':
    app.run(debug=True)