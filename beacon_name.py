from wtforms import Form, BooleanField, TextField, validators
from config import BEACON, DEACTIVATE


class BeaconName(Form):
    """
    BeaconName to deactivate
    """
    beacon_name = TextField('Beacon Name', [validators.Required()])
    accept_details = BooleanField('Are you Sure?', [validators.Required()])

    @staticmethod
    def get_deactivation_url(form):
        """
        Returns URL to deactivate the beacons
        """
        return BEACON + form.beacon_name.data + DEACTIVATE
