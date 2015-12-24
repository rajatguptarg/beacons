import base64
from beacons import Beacon


class EddyStone(Beacon):
    """
    Eddystone beacon protocol
    """
    def advertised_id(self):
        """
        Convert namespace+instance into advertised id
        """
        beacon_id = self.namespace + self.instance
        beacon_id = int(beacon_id, 16)
        return base64.b64encode(self.long_to_bytes(beacon_id))

    def __init__(self, form):
        super(self.__class__, self).__init__(form)
        self.namespace = form.get('namespace')
        self.instance = form.get('instance')
