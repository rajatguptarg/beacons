# pylint: disable-msg=too-many-arguments
class Beacon(object):
    """
    Beacon Details
    """
    def __init__(self, form):
        self.advertised_id = form.get('advid')
        self.beacon_type = form.get('type')
        self.status = form.get('status')
        self.description = form.get('description')
        self.indoorlevel_name = form.get('indoorlevel_name')
        self.latitude = form.get('latitude')
        self.longitude = form.get('longitude')
        self.expected_stability = form.get('expected_stability')
        self.position = form.get('position')
        self.place_id = form.get('place_id')
