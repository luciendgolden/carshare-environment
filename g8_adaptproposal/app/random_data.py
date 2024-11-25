""" dummy driver data creation to feed to decision tree model"""
import os
import random
import json
import numpy as np

# List of driver names
driver_names = ["Alice", "Bob", "Charlie", "David", "Eva", "Frank", "Grace", "Henry", "Isabella", "Jack",
                "Kate", "Leo", "Mila", "Nora", "Oscar", "Penelope", "Quinn", "Ravi", "Samantha", "Thomas",
                "Uma", "Victor", "Wendy", "Xander", "Yara", "Zane", "Ava", "Benjamin", "Chloe", "Daniel",
                "Emily", "Finn", "Gabriella", "Harrison", "Ivy", "Jacob", "Luna", "Michael", "Natalie",
                "Oliver", "Paige", "Quincy", "Rachel", "Sebastian", "Tara", "Vincent", "Willow", "Xavier",
                "Yasmine", "Zara"]
driving_proficiency = ["Beginner", "Inexperienced", "Intermediate", "Advanced", "Expert", "Professional", "Novice",
                       "Skilled",
                       "Competent"]
preferred_route_types = ["City", "Highway", "Mixed", "Rural", "Scenic", "Off-road", "Expressway", "Suburban"]
driving_sickness = ["Yes", "No", "Sometimes", "Rarely", "Occasionally"]
speed_types = ["Slow", "Moderate", "Fast", "Very Fast", "Leisurely"]
comfort_importance = ["Low", "Medium", "High", "Extreme"]
safety_importance = ["Low", "Medium", "High", "Very High", "Top Priority", "Utmost", "Critical"]
police_records = ["Clean", "Minor Infractions", "Traffic Violations", "Clean Record", "Warnings", "Ticketed",
                  "Misdemeanors"]
fuel_type_preference = ["Gasoline", "Diesel", "Hybrid", "Electric"]
transmission_reference = ["Automatic", "Manual"]
off_road_capability = ["Yes", "No"]
family_friendly_features = ["Yes", "No"]

cars = [
    {
        "name": "Toyota Camry",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "High",
            "safety_rating": "High",
            "car_speed": "Moderate",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Mazda MX-5 Miata",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Manual",
            "passenger_capacity": 2,
            "off_road_capability": "No",
            "comfort_rating": "Medium",
            "safety_rating": "Medium",
            "car_speed": "Fast",
            "family_friendly_features": "No"
        }
    },
    {
        "name": "Ford Mustang",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Manual",
            "passenger_capacity": 4,
            "off_road_capability": "No",
            "comfort_rating": "Medium",
            "safety_rating": "Medium",
            "car_speed": "Very Fast",
            "family_friendly_features": "No"
        }
    },
    {
        "name": "Subaru Impreza",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Manual",
            "passenger_capacity": 5,
            "off_road_capability": "Yes",
            "comfort_rating": "Medium",
            "safety_rating": "High",
            "car_speed": "Moderate",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Honda CR-V",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "High",
            "safety_rating": "High",
            "car_speed": "Moderate",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Ford Focus",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "Medium",
            "safety_rating": "Medium",
            "car_speed": "Moderate",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Chevrolet Camaro",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Manual",
            "passenger_capacity": 4,
            "off_road_capability": "No",
            "comfort_rating": "Medium",
            "safety_rating": "Medium",
            "car_speed": "Very Fast",
            "family_friendly_features": "No"
        }
    },
    {
        "name": "Chrysler Pacifica",
        "features": {
            "fuel_type_preference": "Hybrid",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "High",
            "safety_rating": "High",
            "car_speed": "Leisurely",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Volkswagen Jetta",
        "features": {
            "fuel_type_preference": "Diesel",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "High",
            "safety_rating": "High",
            "car_speed": "Moderate",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Tesla Model S",
        "features": {
            "fuel_type_preference": "Electric",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "Extreme",
            "safety_rating": "Top Priority",
            "car_speed": "Very Fast",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "BMW 5 Series",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "High",
            "safety_rating": "Very High",
            "car_speed": "Fast",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Audi A4",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "High",
            "safety_rating": "High",
            "car_speed": "Fast",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Volvo S60",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "High",
            "safety_rating": "Very High",
            "car_speed": "Moderate",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Lexus ES",
        "features": {
            "fuel_type_preference": "Hybrid",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "Extreme",
            "safety_rating": "Top Priority",
            "car_speed": "Moderate",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Subaru Forester",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "Yes",
            "comfort_rating": "High",
            "safety_rating": "High",
            "car_speed": "Moderate",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Mazda CX-5",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "Yes",
            "comfort_rating": "High",
            "safety_rating": "High",
            "car_speed": "Moderate",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Infiniti Q50",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "High",
            "safety_rating": "High",
            "car_speed": "Fast",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Toyota Camry",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "High",
            "safety_rating": "High",
            "car_speed": "Moderate",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Mazda MX-5 Miata",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Manual",
            "passenger_capacity": 2,
            "off_road_capability": "No",
            "comfort_rating": "Medium",
            "safety_rating": "Medium",
            "car_speed": "Fast",
            "family_friendly_features": "No"
        }
    },
    {
        "name": "Ford Mustang",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Manual",
            "passenger_capacity": 4,
            "off_road_capability": "No",
            "comfort_rating": "Medium",
            "safety_rating": "Medium",
            "car_speed": "Very Fast",
            "family_friendly_features": "No"
        }
    },
    {
        "name": "Subaru Impreza",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Manual",
            "passenger_capacity": 5,
            "off_road_capability": "Yes",
            "comfort_rating": "Medium",
            "safety_rating": "High",
            "car_speed": "Moderate",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Honda CR-V",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "High",
            "safety_rating": "High",
            "car_speed": "Moderate",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Ford Focus",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "Medium",
            "safety_rating": "Medium",
            "car_speed": "Moderate",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Chevrolet Camaro",
        "features": {
            "fuel_type_preference": "Gasoline",
            "transmission_reference": "Manual",
            "passenger_capacity": 4,
            "off_road_capability": "No",
            "comfort_rating": "Medium",
            "safety_rating": "Medium",
            "car_speed": "Very Fast",
            "family_friendly_features": "No"
        }
    },
    {
        "name": "Chrysler Pacifica",
        "features": {
            "fuel_type_preference": "Hybrid",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "High",
            "safety_rating": "High",
            "car_speed": "Leisurely",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Volkswagen Jetta",
        "features": {
            "fuel_type_preference": "Diesel",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "High",
            "safety_rating": "High",
            "car_speed": "Moderate",
            "family_friendly_features": "Yes"
        }
    },
    {
        "name": "Tesla Model S",
        "features": {
            "fuel_type_preference": "Electric",
            "transmission_reference": "Automatic",
            "passenger_capacity": 5,
            "off_road_capability": "No",
            "comfort_rating": "Extreme",
            "safety_rating": "Top Priority",
            "car_speed": "Very Fast",
            "family_friendly_features": "Yes"
        }
    },
]


def select_car(selectable_driver, selectable_cars):
    """
    Function pre-selects cars that roughly fit the requirements of the driver,
     to reduce noise in the data
    :param selectable_driver: drivers dictionars
    :param selectable_cars: cars dictionary
    :return: car selected based on conditions and randomness
    """
    while True:
        selectable_car = random.choice(selectable_cars)
        print(selectable_car['name'])
        # checks passenger capacity in relation to passenger amount
        if selectable_car["features"]["passenger_capacity"] >= selectable_driver['passenger_amount']\
                or random.random() < 0.25:
            print(
                f"Condition passenger_capacity: {selectable_car['features']['passenger_capacity']} "
                f">= {selectable_driver['passenger_amount']} is True")
        else:
            print(
                f"Condition passenger_capacity: {selectable_car['features']['passenger_capacity']} "
                f">= {selectable_driver['passenger_amount']} is False")
            continue
        # checks fuel type preference in relation to fuel type of car
        if selectable_car['features']['car_speed'] == selectable_driver['preferred_speed'] \
                or random.random() < 0.5:
            print(
                f"Condition car_speed: {selectable_car['features']['car_speed']} "
                f"== {selectable_driver['preferred_speed']} is True")
        else:
            print(
                f"Condition car_speed: {selectable_car['features']['car_speed']} "
                f"== {selectable_driver['preferred_speed']} is False")
            continue
        # checks driving proficiency in relation to transmission reference (manual or automatic)
        if ((selectable_driver['driving_proficiency'] in ['Beginner', 'Inexperienced', 'Novice'] and
             selectable_car['features']['transmission_reference'] == 'Automatic') or
            (selectable_driver['driving_proficiency'] in ['Intermediate', 'Advanced', 'Expert', 'Professional',
                                                          'Skilled', 'Competent'] and selectable_car['features'][
                 'transmission_reference'] == 'Manual')) or \
                random.random() < 0.50:
            print(
                f"Condition transmission_reference: {selectable_car['features']['transmission_reference']} "
                f"with {selectable_driver['driving_proficiency']} is True")
        else:
            print(
                f"Condition transmission_reference: {selectable_car['features']['transmission_reference']} "
                f"with {selectable_driver['driving_proficiency']} is False")
            continue

        return selectable_car


drivers = []
# back to 10000
for _ in range(10000):
    driver = {
        "driver": random.choice(driver_names),
        "driving_proficiency": random.choice(driving_proficiency),
        "preferred_route_type": random.choice(preferred_route_types),
        "driving_sickness": random.choice(driving_sickness),
        "age": max(18, min(100, int(np.random.normal(35, 10)))),
        "preferred_speed": random.choice(speed_types),
        "passenger_amount": random.randint(2, 5),
        "police_record": random.choice(police_records),

    }
    # Select the car where the passenger_capacity matches the passenger_amount of the driver

    car = select_car(driver, cars)
    driver.update({
        "car": car["name"],
        "comfort_importance": car["features"]["comfort_rating"],
        "safety_importance": car["features"]["safety_rating"],
        # "car_speed": car["features"]["car_speed"],
        "fuel_type_preference": car["features"]["fuel_type_preference"],
        "transmission_reference": car["features"]["transmission_reference"],
        "off_road_capability": car["features"]["off_road_capability"],
        "family_friendly_features": car["features"]["family_friendly_features"]
    })
    drivers.append(driver)

# Saving the generated drivers into a JSON file in the ./sample_data directory
SAMPLE_DATA_DIR = "./sample_data"
os.makedirs(SAMPLE_DATA_DIR, exist_ok=True)

file_path = os.path.join(SAMPLE_DATA_DIR, "generated_drivers.json")
with open(file_path, "w", encoding="utf-8") as json_file:
    json.dump(drivers, json_file, indent=2)

print(f"Generated drivers saved to: {file_path}")
