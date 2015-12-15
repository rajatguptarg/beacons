class Beacon(object):
    """
    Beacon Details
    """
    def __init__(
            self, advertised_id, beacon_type=None, status=None,
            description=None, indoorlevel_name=None, lattitude=None,
            longitude=None, expected_stability=None, position=None,
            place_id=None):
        self.advertised_id = advertised_id
        self.beacon_type = beacon_type
        self.status = status
        self.description = description
        self.indoorlevel_name = indoorlevel_name
        self.lattitude = lattitude
        self.longitude = longitude
        self.expected_stability = expected_stability
        self.position = position
        self.place_id = place_id

    def registration_request_body(self):
        """
        Return the request body in json format
        """
        body = {
            "advertisedId": {
                "type": self.beacon_type,
                "id": self.advertised_id,
            },
            "status": self.status,
            "placeId": self.place_id,
            "latLng": {
                "latitude": self.lattitude,
                "longitude": self.longitude,
            },
            "indoorLevel": {
                "name": self.indoorlevel_name,
            },
            "expectedStability": self.expected_stability,
            "description": self.description,
            "properties": {
                "position": self.position,
            }
        }
        return body
