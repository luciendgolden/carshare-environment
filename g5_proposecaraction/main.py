"""
Main application file.
To run the file with hardcoded input (for testing):
    python main.py
"""
import os, importlib
from fis import fis
from utils.helpers import get_variable_ref as ref
from utils.helpers import get_pretty_action, time_to_decimal
from utils.validators import validate_car_state

# dynamically import variables as modules
for file in os.listdir("variables"):
    # ignore "template.py"
    if file.endswith(".py") and not 'template' in file:
        modul = file[:-3]
        #imported = importlib.import_module(f'variables.{modul}')
        imported = importlib.import_module(f'.{modul}', "variables")
        #print(f'{imported} imported')

# import rules module
importlib.import_module('rules')

def determine_actions(data: dict) -> dict:
    """Propose car action based on input"""
    output = {}
    # get rules from the fis
    for domain_name, (input_list, rule) in fis.rules.items():
        input = {}
        input_str = {}
        # iterate through input list, e.g. ["temperature", "ride time"]
        for var in input_list:
            # populate the empty input dictionary
            # ref(var) returns reference to the module, e. g. variables.temperature
            # getattr gets the Domain object, e. g. temperature from variables.temperature
            input[getattr(ref(var), var)] = data[var]
            input_str[var] = data[var]
        # calculate output and aggregate it into dictionary
        print(f'Input selected for {domain_name}: {input_str}')
        output[domain_name] = rule(input)

    output["car_goes_for_maintenance"] *= 10
    print(f"FIS output: {output}")

    # Interpret FIS output with regular logic
    actions = []
    mvp_action = ("", 0.)
    for domain, value in output.items():
        if value > mvp_action[1] and 'speed_adjustment' not in domain and 'headlight_intensity' not in domain:
            actions = []
            actions.append(get_pretty_action(domain, value)) # append output with the most probability
            mvp_action = (domain, value)

    # Always append headlight_intesity and speed_adjustment
    actions.append(get_pretty_action("headlight_intensity", output.get("headlight_intensity")))
    actions.append(get_pretty_action("speed_adjustment", output.get("speed_adjustment")))
    return {"actions": actions}


# this block will only execute when main.py is run directly (for testing)
if __name__ == "__main__":
    test_input = {
        "temperature": 20,
        "ride_time": 10,
        "fuel": 39,
        "traffic_congestion": 30,
        "visibility": 200,
        "poi": 0.5,
        "car_maintenance_history": 5,
        "daytime": "16:30"
    }


    if not validate_car_state(test_input):
        print("Invalid input.")
        raise KeyError
    
    test_input["daytime"] = time_to_decimal(test_input["daytime"])

    actions = determine_actions(test_input)
    print("Actions: ", actions)
