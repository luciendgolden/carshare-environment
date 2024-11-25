from flask import Flask, request, jsonify, send_from_directory, abort, Response
from flask_cors import CORS
from flasgger import Swagger
from collections import OrderedDict


from config import Config
from dijkstra import dijkstra, create_graph, reconstruct_path
from strassen import strassen

import json
import requests
import datetime
import subprocess
import logging
import os

app = Flask(__name__)
CORS(app)

app.config['SWAGGER'] = {
    'openapi': '3.0.0'
}

template_path = os.path.join(app.root_path, 'openapi.yaml')
swagger = Swagger(app, template_file=template_path)

logging.basicConfig(level=logging.DEBUG)

def get_current_time_parameters():
    now = datetime.datetime.now()
    day_of_week = now.strftime("%A").lower()
    hour = now.hour

    if 6 <= hour < 12:
        time_of_day = "morning"
    elif hour == 12:
        time_of_day = "noon"
    elif 12 < hour < 18:
        time_of_day = "afternoon"
    elif 18 <= hour < 22:
        time_of_day = "evening"
    else:
        time_of_day = "night"

    return day_of_week, time_of_day

def get_weather(location='Vienna'):
    api_key = Config.OPEN_WEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    try:
        response = requests.get(url, timeout=5) 
        response.raise_for_status()
        weather_data = response.json()
        weather_main = weather_data['weather'][0]['main'].lower()
        
        if 'rain' in weather_main:
            return 'rainy'
        elif 'clear' in weather_main:
            return 'sunny'
        else:
            return weather_main
    except requests.Timeout:
        app.logger.error("Weather API request timed out.")
        return 'unknown'
    except requests.RequestException as e:
        app.logger.error(f"Weather API request failed: {e}")
        return 'unknown'


def main(customer_position, destination_position, car_positions):
    graph, movements = create_graph(strassen)
    car_distances = {}
    car_destination_distances = {}
    car_destination_paths = {}

    app.logger.debug(f'Graph: {graph}')

    for car, position in car_positions.items():
        # Calculate the shortest path from the car's position to the customer's position
        distance, predecessors = dijkstra(graph, position, customer_position)
        car_distances[car] = (distance, reconstruct_path(predecessors, position, customer_position))

        # Calculate the shortest path from the car's position to the destination position
        destination_distance, destination_predecessors = dijkstra(graph, position, destination_position)
        car_destination_distances[car] = destination_distance
        car_destination_paths[car] = reconstruct_path(destination_predecessors, position, destination_position)

    # Calculate the shortest path from the customer's position to the destination
    customer_destination_distance, customer_destination_predecessors = dijkstra(graph, customer_position, destination_position)
    customer_destination_path = reconstruct_path(customer_destination_predecessors, customer_position, destination_position)

    # Sort cars by their distance to the customer
    sorted_cars = sorted(car_distances.items(), key=lambda x: x[1][0])

    nearest_car, nearest_info = sorted_cars[0]
    nearest_distance, nearest_path = nearest_info

    second_nearest_car, second_nearest_info = sorted_cars[1] if len(sorted_cars) > 1 else (None, (float('infinity'), []))
    second_nearest_distance, second_nearest_path = second_nearest_info

    third_nearest_car, third_nearest_info = sorted_cars[2] if len(sorted_cars) > 2 else (None, (float('infinity'), []))
    third_nearest_distance, third_nearest_path = third_nearest_info

    app.logger.debug(f"Nearest Car: {nearest_car}, Path: {nearest_path}, Distance: {nearest_distance}")
    app.logger.debug(f"Second Nearest Car: {second_nearest_car}, Path: {second_nearest_path}, Distance: {second_nearest_distance}")
    app.logger.debug(f"Third Nearest Car: {third_nearest_car}, Path: {third_nearest_path}, Distance: {third_nearest_distance}")

    app.logger.debug(f"Customer to Destination Distance: {customer_destination_distance}")
    app.logger.debug(f"Customer to Destination Path: {customer_destination_path}")

    app.logger.debug(f"Car to Destination Distances: {car_destination_distances}")
    app.logger.debug(f"Car to Destination Paths: {car_destination_paths}")

    # Correctly generate the car movements based on the path
    nearest_car_movements = [(start, end, movements[(start, end)]) for start, end in zip(nearest_path[:-1], nearest_path[1:])]
    customer_destination_movements = [(start, end, movements[(start, end)]) for start, end in zip(customer_destination_path[:-1], customer_destination_path[1:])]

    return nearest_car, nearest_path, nearest_distance, nearest_car_movements, second_nearest_car, second_nearest_path, second_nearest_distance, third_nearest_car, third_nearest_path, third_nearest_distance, customer_destination_distance, customer_destination_path, customer_destination_movements, car_destination_distances, car_destination_paths, movements

@app.route('/')
def index():
    return jsonify({'message': 'g4_determinepickup', 'success': True })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'UP'}), 200

@app.route('/files/<path:filename>')
def serve_file(filename):
    try:
        return send_from_directory(app.static_folder, filename)
    except FileNotFoundError:
        abort(404)

@app.route('/determinePickUp', methods=['POST', 'OPTIONS'])
def determine_pickup():
    if request.method == 'OPTIONS':
        app.logger.info("Received OPTIONS request")
        return jsonify(success=True)
    
    data = request.json
    app.logger.info(f"Incoming request data: {data}")

    customer_position = data.get('customer_position')
    destination_position = data.get('destination_position')
    car_positions = {
        'Car 1': data.get('car1_position'),
        'Car 2': data.get('car2_position'),
        'Car 3': data.get('car3_position'),
    }
    traffic = data.get('traffic').strip()
    local_events = data.get('local_events').strip()
    road_constructions_input = data.get('road_constructions').strip()
    road_constructions = road_constructions_input.split(",") if road_constructions_input else []
    age = data.get('age')
    gender = data.get('gender').strip()
    account_type = data.get('account_type').strip()
    
    if not all([customer_position, destination_position, *car_positions.values(), traffic, local_events, road_constructions, age, gender, account_type]):
        return jsonify({'error': 'Missing parameters!'}), 400

    day_of_week, time_of_day = get_current_time_parameters()
    weather = get_weather()

    nearest_car, nearest_path, nearest_distance, nearest_car_movements, second_nearest_car, second_nearest_path, second_nearest_distance, third_nearest_car, third_nearest_path, third_nearest_distance, customer_destination_distance, customer_destination_path, customer_destination_movements, car_destination_distances, car_destination_paths, movements = main(customer_position, destination_position, car_positions)

    prolog_road_constructions = "[" + ", ".join(f"'{node}'" for node in road_constructions) + "]"

    app.logger.debug(f"Prolog Query Data: customer_destination_distance={customer_destination_distance}, car_destination_distances={car_destination_distances}, car_destination_paths={car_destination_paths}, weather={weather}, traffic={traffic}, local_events={local_events}, road_constructions={prolog_road_constructions}, time_of_day={time_of_day}, day_of_week={day_of_week}, age={age}, gender={gender}, account_type={account_type}, customer_position={customer_position}, destination_position={destination_position}, nearest_car={nearest_car}, second_nearest_car={second_nearest_car}, third_nearest_car={third_nearest_car}")

    prolog_query = f"""
    consult('rules.pl'),
    optimal_pickup(
        {customer_destination_distance},
        {car_destination_distances['Car 1']}, {car_destination_paths['Car 1']},
        {car_destination_distances['Car 2']}, {car_destination_paths['Car 2']},
        {car_destination_distances['Car 3']}, {car_destination_paths['Car 3']},
        {nearest_path}, {nearest_distance},
        {second_nearest_path}, {second_nearest_distance},
        {third_nearest_path}, {third_nearest_distance},
        weather({weather}), traffic({traffic}), local_events({local_events}),
        road_constructions({prolog_road_constructions}),
        time_of_day({time_of_day}), day_of_week({day_of_week}),
        {age}, gender({gender}), account_type({account_type}),
        '{customer_position}', '{destination_position}',
        '{nearest_car}', '{second_nearest_car}', '{third_nearest_car}',
        Location, Rule
    ),
    writeln(Location),
    writeln(Rule),
    halt.
    """

    app.logger.info(f"Executing Prolog Query: {prolog_query}")

    result = subprocess.run(['swipl', '-q', '-g', prolog_query, '-t', 'halt(1)', '-'], capture_output=True, text=True)

    if result.returncode != 0:
        app.logger.error(f'Prolog command failed: {result.stderr}')

    output = result.stdout.strip().split('\n')

    app.logger.debug(f"Prolog Output: {output}")
    app.logger.error(f"Prolog Execution Error (if any): {result.stderr}")

    location = output[0] if len(output) > 0 else ""
    rule = output[1] if len(output) > 1 else "Unknown Rule"

    # Determine the correct path and movements for the selected car
    if location == nearest_car:
        path_to_return = nearest_path
        customer_car_distance = nearest_distance
    elif location == second_nearest_car:
        path_to_return = second_nearest_path
        customer_car_distance = second_nearest_distance
    elif location == third_nearest_car:
        path_to_return = third_nearest_path
        customer_car_distance = third_nearest_distance
    else:
        path_to_return = []
        customer_car_distance = 0

    # Construct movements for the selected car path
    car_movements_to_return = [(start, end, movements[(start, end)]) for start, end in zip(path_to_return[:-1], path_to_return[1:]) if (start, end) in movements]
    car_movements_dict = OrderedDict((f"{start}_{end}", move) for start, end, move in car_movements_to_return)
    app.logger.debug(f"Car Movements Dictionary: {car_movements_dict}")

    # Construct movements for the customer to destination path
    customer_movements_to_return = [(start, end, movements[(start, end)]) for start, end in zip(customer_destination_path[:-1], customer_destination_path[1:]) if (start, end) in movements]
    customer_movements_dict = OrderedDict((f"{start}_{end}", move) for start, end, move in customer_movements_to_return)
    app.logger.debug(f"Customer Movements Dictionary: {customer_movements_dict}")


    parameters_used = {
        'customer_position': customer_position,
        'destination_position': destination_position,
        'car1_position': car_positions['Car 1'],
        'car2_position': car_positions['Car 2'],
        'car3_position': car_positions['Car 3'],
        'weather_location': 'Vienna',
        'weather': weather,
        'traffic': traffic,
        'local_events': local_events,
        'road_constructions': road_constructions_input,
        'time_of_day': time_of_day,
        'day_of_week': day_of_week,
        'age': age,
        'gender': gender,
        'account_type': account_type,
        'customer_destination_distance': customer_destination_distance,
        'car_destination_distances': car_destination_distances,
        'car_destination_paths': car_destination_paths,
        'nearest_car': nearest_car,
        'second_nearest_car': second_nearest_car,
        'third_nearest_car': third_nearest_car,
    }

    response_data = {
        'optimal_pickup': location, 
        'car route': path_to_return, 
        'car movements': car_movements_dict,
        'distance to nearest car': customer_car_distance, 
        'distance to destination': customer_destination_distance,
        'customer to destination path': customer_destination_path,
        'customer movements': customer_movements_dict,
        'Rule': rule,
        'parameters_used': parameters_used
    }

    response_json = json.dumps(response_data, sort_keys=False)
    return Response(response_json, content_type='application/json')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8084, debug=True)
