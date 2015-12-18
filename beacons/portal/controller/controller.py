#!/usr/bin/env python
from config import REGISTER_BEACONS, ERROR, SUCCESS
import json
import requests
from beacons.portal.helper import BeaconHelper, URLBuilder
from beacons.portal.models import Header

beacon_helper = BeaconHelper()
url_builder = URLBuilder()


def register_beacon(beacon, credentials):
    """
    Retun the response
    """
    request_body = beacon.registration_request_body()
    header = Header(credentials.access_token)
    response = requests.post(REGISTER_BEACONS, data=json.dumps(request_body),
        headers=header.get_header_body())
    return response.content


def deactivate_beacon(beacon_details, credentials):
    """
    Retun the response
    """
    header = Header(credentials.access_token)
    url = url_builder.beacon_deactivation_url(beacon_details)
    response = requests.post(url, headers=header.get_header_body())
    status = ERROR if response.status_code is 400 else SUCCESS
    return status


def attachdatato_beacon(beacon_details, credentials):
    """
    Retun the response
    """
    request_body = beacon_details.attachment_request_body()
    header = Header(credentials.access_token)
    url = url_builder.beacon_attachment_url(beacon_details)
    response = requests.post(url, data=json.dumps(request_body),
        headers=header.get_header_body())
    return response.content


def modify_beacon(beacon, credentials):
    """
    Modify the details of existing beacons
    """
    header = Header(credentials.access_token)
    request_body = beacon.update_request_body()
    url = url_builder.beacon_modification_url(beacon)
    response = requests.put(url, data=json.dumps(request_body),
        headers=header.get_header_body())
    return response.content
