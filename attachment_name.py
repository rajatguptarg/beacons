from wtforms import Form, TextField, validators
from config import ATTACH, ATTACH_BEACONS


class BeaconAttachmentName(Form):
    """
    BeaconName to which we need to add attachment
    """
    beacon_name = TextField('Beacon Name', [validators.Required()])

    @staticmethod
    def get_attachment_url(form):
        """
        Returns URL to attach the beacons
        """
        return ATTACH_BEACONS + form.beacon_name.data + ATTACH
