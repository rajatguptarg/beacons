class Beacon(object):
    """
    Beacon Details
    """
    def __init__(self, advertised_id):
        self.advertised_id = advertised_id
        self.beacon_type = None
        self.status = None
        self.description = None
        self.indoorlevel_name = None
        self.lattitude = None
        self.longitude = None
        self.expected_stability = None
        self.position = None
        self.place_id = None

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
