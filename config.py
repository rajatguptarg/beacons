# List of all the URLs
import os

LIST_BEACONS = \
    'https://proximitybeacon.googleapis.com/v1beta1/beacons?pageSize=100'

SCOPE = 'https://www.googleapis.com/auth/userinfo.profile \
    https://www.googleapis.com/auth/userlocation.beacon.registry'

REGISTER_BEACONS = \
    'https://proximitybeacon.googleapis.com/v1beta1/beacons:register'

BEACON = 'https://proximitybeacon.googleapis.com/v1beta1/'

DEACTIVATE = ':deactivate'

NAMESPACE = 'https://proximitybeacon.googleapis.com/v1beta1/namespaces'

ATTACH = '/attachments'

ERROR = 'ERROR'

SUCCESS = 'SUCCESS'

USER_INFO = 'https://www.googleapis.com/oauth2/v1/userinfo'

ESTIMOTE_CMD = \
    "curl -u " + str(os.environ.get('estimote_username')) + ":" + \
    str(os.environ.get('estimote_password')) + \
    " -H 'Accept: application/json' https://cloud.estimote.com/v1/beacons"
