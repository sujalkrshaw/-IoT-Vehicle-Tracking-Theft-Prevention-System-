import math

SAFE_LAT = 22.5726
SAFE_LON = 88.3639
SAFE_RADIUS = 0.001


def calculate_distance(lat1, lon1, lat2, lon2):
    return math.sqrt(
        (lat2 - lat1) ** 2 +
        (lon2 - lon1) ** 2
    )


def is_outside_geofence(lat, lon):
    distance = calculate_distance(
        SAFE_LAT,
        SAFE_LON,
        lat,
        lon
    )

    return distance > SAFE_RADIUS