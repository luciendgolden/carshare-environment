import re

def validate_car_state(data):
    try:
        if not (0 <= data['temperature'] < 40): return False
        if not (0 <= data['ride_time'] < 60): return False
        if not (0 <= data['fuel'] < 40): return False
        if not (0 <= data['traffic_congestion'] < 50): return False
        if not (20 <= data['visibility'] < 250): return False
        if not (0 <= data['poi'] < 1): return False
        if not (0 <= data['car_maintenance_history'] < 10): return False
        if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', data['daytime']): return False
        return True
    except KeyError:
        return False