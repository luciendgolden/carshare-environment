from fuzzylogic.classes import Set

accuracy = 0.01 # optionally omit values smaller than this value

legal_speed_limit = 50; # 50 km/h -> Legal speed limit in Vienna city (assuming driving Within city area)

def pretty_print_weights(sets: list[tuple[Set, float]], omit_zeros=False) -> None:
    """Print membership values for weights"""
    for name, value in sets:
        if (not omit_zeros or (omit_zeros and value > accuracy)):
            print(f"{name}: {value}")

def get_variable_ref(module_name: str):
    if 'variables' in module_name:
        return __import__(module_name, fromlist=[''])
    return __import__(f'variables.{module_name}', fromlist=[''])

def time_to_decimal(time_str):
    hours, minutes = map(int, time_str.split(':'))
    return hours + minutes / 60.0

def get_pretty_action(domain: str, value: float):
    result = {"name": domain, "value": round(value,2)}
    if "gas_station" in domain:
        if value > 66:
            result["incentive"]=  f"10 EUR gift card"
        elif value > 20:
            result["incentive"] = f"10% discount"
    elif "ride_sharing" in domain:
        if value > 30:
            result["incentive"] = f"10% for the ride"
        if value > 60:
            result["incentive"] = f"25% for the ride"
    elif "speed_adjustment" in domain:
        # Overriding value for speed_adjustment to return the recommended speed for that route using the recommended percentage * legal limit
        # Note: In presentation video it is returned as percentage
        result["value"] = round(value * legal_speed_limit / 100,2)
        result["unit"] = "km/h"
    elif "headlight_intensity" in domain:
        result["unit"] = "%"
    return result