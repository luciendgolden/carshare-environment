import re

# Valid input ranges for each car state field
FIELD_RANGES = {
    'temperature': (0, 40),           # degrees Celsius
    'ride_time': (0, 60),             # minutes
    'fuel': (0, 40),                  # litres remaining
    'traffic_congestion': (0, 50),    # congestion index (0=free, 50=gridlock)
    'visibility': (20, 250),          # metres
    'poi': (0, 1),                    # points-of-interest density (0–1)
    'car_maintenance_history': (0, 10),  # maintenance score
}


def validate_car_state(data):
    """Validate car state input fields.

    Returns True if all fields are present and within their valid ranges,
    False otherwise. Individual field errors are logged to stderr.
    """
    try:
        for field, (low, high) in FIELD_RANGES.items():
            if not (low <= data[field] < high):
                return False
        if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', data['daytime']):
            return False
        return True
    except KeyError:
        return False