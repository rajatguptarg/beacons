from wtforms import Form, BooleanField, TextField, validators


class Beacon(Form):
    """
    Beacon Details
    """
    advertised_id = TextField('Advertised ID', [validators.Required()])
    status = TextField('ACTIVE')
    beacon_type = TextField('EDDYSTONE')
    description = TextField('Description')
    indoorlevel_name = TextField('Indoor Level Name')
    lattitude = TextField('Lattitude')
    longitude = TextField('Longitude')
    expected_stability = TextField('Expected Stability')
    position = TextField('Position')
    place_id = TextField('Place Id')
    accept_details = BooleanField('Are you sure!', [validators.Required()])

    @staticmethod
    def registration_request_body(form):
        """
        Return the request body in json format
        """
        body = {
            "advertisedId": {
                "type": form.beacon_type.data,
                "id": form.advertised_id.data,
            },
            "status": form.status.data,
            "placeId": form.place_id.data,
            "latLng": {
                "latitude": form.lattitude.data,
                "longitude": form.longitude.data,
            },
            "indoorLevel": {
                "name": form.indoorlevel_name.data,
            },
            "expectedStability": form.expected_stability.data,
            "description": form.description.data,
            "properties": {
                "position": form.position.data,
            }
        }
        return body
