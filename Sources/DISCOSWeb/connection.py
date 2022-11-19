# Constructs a DISCOSWeb query with the given parameters.



import requests

from .filtering import APIFilter

from pprint import pprint
from typing import Optional



class APIConnection:
    def __init__(self, token: str):
        # Check the validity of the authentication token.
        if type(token) is not str:
            raise ValueError("A Connection to the DISCOSWeb API Server must have a valid authentication token")

        # Store the token.
        self.token = token

        # Build the object cache.
        self.cache = {}

    def url(self, filter: Optional[APIFilter] = None) -> str:
        """Buils the full URL to perform this query"""

        return f"https://discosweb.esoc.esa.int/api/objects?filter={ filter.apistring() }"

    def request(self, filter: Optional[APIFilter] = None):
        """Requests a query response from the DISCOSWeb API server"""

        # Constant URL of the API.
        URL = 'https://discosweb.esoc.esa.int'

        # Perform the request and get its JSON representation.
        response = requests.get(
            f'{URL}/api/objects',
            headers={
                'Authorization': f'Bearer {self.token}',
                'DiscosWeb-Api-Version': '2',
            },
            params={
                'filter': f"{filter.apistring()}"
            },
        )

        data = response.json()

        # Check if the response failed.
        if not response.ok:
            pprint(data['errors'])
