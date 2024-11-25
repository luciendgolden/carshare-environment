import math

# https://github.com/sidnircarlos/heaversine/blob/master/haversine.ipynb
def calculate_distance(lat1, lon1, lat2, lon2):
    # lat and lon from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    # Radius of earth in km
    r = 6371
    return c * r

def is_remote(start_lat, start_lon, end_lat, end_lon, central_lat, central_lon, threshold_km):
    distance_start = calculate_distance(start_lat, start_lon, central_lat, central_lon)
    distance_end = calculate_distance(end_lat, end_lon, central_lat, central_lon)

    return distance_start > threshold_km or distance_end > threshold_km
