from beacons.portal.models import Beacon, BeaconName, Header
from config import BEACON, DEACTIVATE


class BeaconHelper(object):
    """
    docstring for BeaconHelper
    """
    def create_beacon(self, form):
        """
        Create the beacon from form data
        """
        beacon = Beacon(form.get('advid'))
        beacon.beacon_type = form.get('type')
        beacon.status = form.get('status')
        beacon.description = form.get('description')
        beacon.indoorlevel_name = form.get('indoorlevel_name')
        beacon.latitude = form.get('latitude')
        beacon.longitude = form.get('longitude')
        beacon.expected_stability = form.get('expected_stability')
        beacon.position = form.get('position')
        beacon.place_id = form.get('place_id')
        return beacon

    def create_beacon_name(self, form):
        """
        Create beacon name object
        """
        beacon_details = BeaconName(form.get('name'))
        return beacon_details

    def registration_request_body(self, beacon):
        """
        Return the request body in json format
        """
        body = {
            "advertisedId": {
                "type": beacon.beacon_type,
                "id": beacon.advertised_id,
            },
            "status": beacon.status,
            "placeId": beacon.place_id,
            "latLng": {
                "latitude": beacon.latitude,
                "longitude": beacon.longitude,
            },
            "indoorLevel": {
                "name": beacon.indoorlevel_name,
            },
            "expectedStability": beacon.expected_stability,
            "description": beacon.description,
            "properties": {
                "position": beacon.position,
            }
        }
        return body

    def get_deactivation_url(self, beacon_details):
        """
        Returns URL to deactivate the beacons
        """
        return BEACON + beacon_details.beacon_name + DEACTIVATE

    def get_header(self, access_token):
        """
        Returns the header of the request
        """
        header = Header(access_token)

        header_body = {
            'Authorization': 'Bearer ' + header.access_token
        }
        return header_body

    def __init__(self):
        super(BeaconHelper, self).__init__()
