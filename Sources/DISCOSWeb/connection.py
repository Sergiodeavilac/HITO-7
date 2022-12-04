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

        if filter is not None:
            return f"https://discosweb.esoc.esa.int/api/objects?filter={ filter.apistring() }"
        else:
            return f"https://discosweb.esoc.esa.int/api/objects"

    def orbits(self, epoch=None):
        # Constant URL of the API.
        URL = 'https://discosweb.esoc.esa.int'

        # Get the epoch filter.
        if epoch is not None:
            filter = f"gt(epoch,epoch:'{epoch}')"
        else:
            filter = "gt(epoch,epoch:'2010-01-01 12:00')"

        # Perform the request.
        response = requests.get(
            f'{URL}/api/destination-orbits',
            headers={
                'Authorization': f'Bearer {self.token}',
                'DiscosWeb-Api-Version': '2',
            },
            params={
                'filter': filter,
                'page[size]': '30',
            },
        )

        data = response.json()
        pointed = response.url

        # Check if the response failed.
        if not response.ok:
            pprint(data['errors'])

        return data, pointed

    def orbitparams(self, id: int):
        # Constant URL of the API.
        URL = 'https://discosweb.esoc.esa.int'

        # Perform the request.
        response = requests.get(
            f'{URL}/api/objects/{id}/destination-orbits',
            headers={
                'Authorization': f'Bearer {self.token}',
                'DiscosWeb-Api-Version': '2',
            },
            params={
                'page[size]': '100',
            },
        )

        data = response.json()

        # Check if the response failed.
        if not response.ok:
            pprint(data['errors'])
        else:
            pprint(data['data'])

        return data['data']


    def objects(self, filter: APIFilter):
        """Requests a query response from the DISCOSWeb API server"""

        # Constant URL of the API.
        URL = 'https://discosweb.esoc.esa.int'

        print(f"Searching filter: {filter.apistring()}")

        # Perform the request and get its JSON representation.
        response = requests.get(
            f'{URL}/api/destination-orbits',
            headers={
                'Authorization': f'Bearer {self.token}',
                'DiscosWeb-Api-Version': '2',
            },
            params={
                'filter': f"{filter.apistring()}",
                'page[size]': '100',
            },
        )

        data = response.json()

        # Check if the response failed.
        if not response.ok:
            pprint(data['errors'])
        else:
            pprint(data)
            return data['data']
