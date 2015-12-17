#!/usr/bin/env python
from config import REGISTER_BEACONS, ERROR, SUCCESS
import json
import requests
from beacons.portal.helper import BeaconHelper


beacon_helper = BeaconHelper()


def send_registration_request(beacon, credentials):
    """
    Retun the response
    """
    request_body = beacon_helper.registration_request_body(beacon)
    response = requests.post(REGISTER_BEACONS, data=json.dumps(request_body),
        headers=beacon_helper.get_header(credentials.access_token))
    return response.content


def send_deactivation_request(beacon_details, credentials):
    """
    Retun the response
    """
    url = beacon_helper.get_deactivation_url(beacon_details)
    response = requests.post(url,
        headers=beacon_helper.get_header(credentials.access_token))
    status = ERROR if response.status_code is 400 else SUCCESS
    return status
