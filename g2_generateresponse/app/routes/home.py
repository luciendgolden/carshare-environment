from flask import Blueprint, jsonify

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/')
def home():
    # home json root response
    json_response = jsonify({
        "message": "Welcome to the G2 Generate Response Service",
        "success": True
    })

    return json_response
