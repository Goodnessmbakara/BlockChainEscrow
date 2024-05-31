from google.auth.transport import requests
from google.oauth2 import id_token

class Google:
    """
    Google class to fetch the user info and return it
    """
    @staticmethod
    def validate(auth_token):
        """
        Queries the google oAUTH api to fetch the user info
        """
        try:
            idinfo = id_token.verify_oauth_token(
                auth_token,requests.Request()
            )
            if 'account.google.com' in idinfo['iss']:
                return idinfo
        except:
            return "The Token is either invalid or expired"