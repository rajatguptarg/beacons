from binascii import unhexlify
import base64


class BeaconHelper(object):
    """
    Helper of Beacons
    """
    def _long_to_bytes(self, value, endianness='big'):
        """
        Convert hexadecimal into byte array
        """
        width = value.bit_length()
        width += 8 - ((width % 8) or 8)
        fmt = '%%0%dx' % (width // 4)
        s = unhexlify(fmt % value)

        if endianness == 'little':
            s = s[::-1]

        return s

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
