from flask import Blueprint, jsonify, request
from services import PricingGAService, CustomerService, CustomerPricingService
from utils import weather_module, remoteness_module

import logging
import datetime
import os
import math

OPEN_WEATHER_API_KEY = os.environ.get('OPEN_WEATHER_API_KEY')

pricing_blueprint = Blueprint('pricing', __name__)

@pricing_blueprint.route('/pricing/company', methods=['POST'])
def calculate_price():
    try:
        data = request.get_json()
        today = datetime.datetime.now()
        day_of_week = today.weekday()

        # Extract options for remoteness
        options = data.get('options', {})
        central_point_latitude = options.get('central_point', {}).get('lat')
        central_point_longitude = options.get('central_point', {}).get('lon')
        threshold_km = options.get('threshold_km', 0)

        if not options or not central_point_latitude or not central_point_longitude or not threshold_km:
            return jsonify({'error': 'Missing required options'}), 400

        # Extract trip data
        trip = data.get('trip', {})
        start_latitude = trip.get('start', {}).get('lat')
        start_longitude = trip.get('start', {}).get('lon')
        end_latitude = trip.get('end', {}).get('lat')
        end_longitude = trip.get('end', {}).get('lon')

        # GA parameters
        parameters = data.get('parameters', {})

        remoteness = remoteness_module.is_remote(
                start_latitude, start_longitude,
                end_latitude, end_longitude,
                central_point_latitude, central_point_longitude,
                threshold_km)

        # weather condition
        weather = weather_module.get_weather(OPEN_WEATHER_API_KEY, start_latitude, start_longitude)

        if weather.get('cod') == 200:
            weather_condition = weather_module.evaluate_weather(weather)
        else:
            weather_condition = 'moderate'

        # Run GA
        ga_service = PricingGAService(
            customer_loyalty=parameters.get('customer_loyalty', 0),
            weather_condition=parameters.get('weather_condition', weather_condition),
            day_of_week=parameters.get('day_of_week', day_of_week),
            remoteness=parameters.get('remoteness', remoteness),
            base_price=parameters.get('base_price', 1.0),
            loyalty_discount=parameters.get('loyalty_discount', 0.1),
            weather_surcharge=parameters.get('weather_surcharge', 1.2),
            weekend_surcharge=parameters.get('weekend_surcharge', 1.1),
            remoteness_surcharge=parameters.get('remoteness_surcharge', 1.15)
        )

        best_individual, best_price = ga_service.run()

        days_of_week = {
            0: "Monday",
            1: "Tuesday",
            2: "Wednesday",
            3: "Thursday",
            4: "Friday",
            5: "Saturday",
            6: "Sunday"
        }

        customer_loyalty_bool = bool(parameters.get('customer_loyalty', 0))
        day_of_week_name = days_of_week.get(parameters.get('day_of_week', day_of_week), "Unknown Day")
        remoteness_bool = bool(parameters.get('remoteness', remoteness))

        return jsonify({
            'best_price': round(best_price, 2),
            'currency': 'EUR',
            'currency_symbol': '€',
            # profit is price - cost
            'profit': round(best_price - parameters.get('base_price', 1.0), 2),
            # profit percentage is profit / cost * 100
            'profit_percentage': round((best_price - parameters.get('base_price', 1.0)) / parameters.get('base_price', 1.0) * 100, 2),
            'best_individual': best_individual,
            'parameters': {
                'customer_loyalty': customer_loyalty_bool,
                'weather_condition': parameters.get('weather_condition', weather_condition),
                'day_of_week': day_of_week_name,
                'remoteness': remoteness_bool,
                'base_price': parameters.get('base_price', 1.0),
                'loyalty_discount': parameters.get('loyalty_discount', 0.1),
                'weather_surcharge': parameters.get('weather_surcharge', 1.2),
                'weekend_surcharge': parameters.get('weekend_surcharge', 1.1),
                'remoteness_surcharge': parameters.get('remoteness_surcharge', 1.15)
            },
        })

    except KeyError as e:
        logging.error(f"Key error: {e}")
        return jsonify({'error': 'Missing required data'}), 400
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred processing your request'}), 500


@pricing_blueprint.route('/pricing/costs', methods=['POST'])
def calculate_cost():
    try:
        #Extract parameters for function call
        data = request.get_json()


        lat_start = data.get('start', {}).get('lat')
        lon_start = data.get('start', {}).get('lon')

        lat_destination = data.get('destination', {}).get('lat')
        lon_destination = data.get('destination', {}).get('lon')

        car_class = data.get('car_class',{})
        total_km = data.get('total_km',{})

        if not lat_start or not lon_start or not lat_destination or not lon_destination or not car_class or not total_km:
            return jsonify({'error': 'Missing required options'}), 400



        start_x = (lat_start,lon_start)
        dest_x = (lat_destination, lon_destination)

        customer_service = CustomerService()

        # Run GA
        best_individual, lowest_cost = customer_service.run_optimization((lat_start, lon_start), (lat_destination, lon_destination), car_class, total_km)



        return jsonify({
            'lowest_cost': round(lowest_cost[0], 2),
            'best_individual': best_individual,
            'parameters': {
                'start':{
                'lat': lat_start,
                'lon': lon_start,
                },
                'destination':{
                'lat': lat_destination,
                'lon': lon_destination,
                },
                'car_class': car_class,
                'total_km': total_km,
            },
        })

    except KeyError as e:
        logging.error(f"Key error: {e}")
        return jsonify({'error': 'Missing required data'}), 400
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred processing your request'}, 500)

@pricing_blueprint.route('/pricing/customer', methods=['POST'])
def calculate_customer():
    try:
        #Extract parameters for function call
        data = request.get_json()

        customer_rate = data.get('customer_rate', {})
        car_class = data.get('car_class', {})
        base_price = data.get('base_price', {})
        car_location = data.get('car_location', {})
        customer_location = data.get('customer_location', {})
        destination_location = data.get('destination_location', {})


        if not customer_rate or not car_class or not base_price or not car_location or not customer_location or not destination_location:
            return jsonify({'error': 'Missing required options'}), 400


        customer_service = CustomerPricingService(customer_rate,car_class,base_price,car_location,customer_location,destination_location)

        # Run GA
        return customer_service.run()

    except KeyError as e:
        logging.error(f"Key error: {e}")
        return jsonify({'error': 'Missing required data'}), 400
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred processing your request'}, 500)
