class Beacon(object):
    """
    Beacon Details
    """
    def __init__(
            self, advertised_id, beacon_type=None, status=None,
            description=None, indoorlevel_name=None, latitude=None,
            longitude=None, expected_stability=None, position=None,
            place_id=None):
        self.advertised_id = advertised_id
        self.beacon_type = beacon_type
        self.status = status
        self.description = description
        self.indoorlevel_name = indoorlevel_name
        self.latitude = latitude
        self.longitude = longitude
        self.expected_stability = expected_stability
        self.position = position
        self.place_id = place_id
