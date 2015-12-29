import base64
from beacons.portal.models import IBeacon, EddyStone


class BeaconHelper(object):
    """
    Helper of Beacons
    """
    @staticmethod
    def create_beacon(form):
        """
        Return appropiate beacon
        """
        if form.get('type') == 'iBEACON':
            return IBeacon(form)
        return EddyStone(form)

    def get_adverised_id(self, beacon_id):
        """
        Convert namespace+instance into advertised id
        """
        beacon_id = int(beacon_id, 16)
        return base64.b64encode(self._long_to_bytes(beacon_id))

    def get_namespace_instance(self, advertised_id):
        """
        Returns namespace and instance id of beacon
        """
        advertised_id = base64.b64decode(advertised_id)
        advertised_id = int(advertised_id.encode('hex'), 16)
        namespace_instance = hex(advertised_id)[2:-1]
        namespace = namespace_instance[:20]
        instance = namespace_instance[-12:]
        return namespace, instance

    def __init__(self):
        super(BeaconHelper, self).__init__()
