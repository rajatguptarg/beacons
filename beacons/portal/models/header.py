class Header(object):
    """
    OAuth2.0 Header Details
    """
    def get_header_body(self):
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
        return self.get_header_body()
