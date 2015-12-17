class BeaconName(object):
    """
    BeaconName to deactivate
    """
    def __init__(self, beacon_name_dict):
        self.beacon_name = beacon_name_dict.get('name')
