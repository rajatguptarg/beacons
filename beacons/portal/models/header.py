class Header(object):
    """
    OAuth2.0 Header Details
    """
    access_token = ''

    def get_header(self):
        """
        Returns the header of the request
        """
        header = {
            'Authorization': 'Bearer ' + self.access_token
        }
        return header

    def __init__(self, access_token):
        self.access_token = access_token

    def __str__(self):
        return self.get_header()
