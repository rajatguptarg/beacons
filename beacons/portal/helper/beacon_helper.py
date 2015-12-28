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

    def __init__(self):
        super(BeaconHelper, self).__init__()
