# Test the default example for the API.

from pprint import pprint
import requests



# Web address and access token.
URL = 'https://discosweb.esoc.esa.int'
token = 'IjI1ZmVjYjBlLWIwNDQtNDVmNS1hODY2LTI3Njg5MzExZDQzZSI.1skiwOZt0Vw6jgsxlAPW3y4YtV8'

# Perform the request.
response = requests.get(
    f'{URL}/api/objects',
    headers={
        'Authorization': f'Bearer {token}',
        'DiscosWeb-Api-Version': '2',
    },

    params={
        'filter': "eq(objectClass,Payload)&gt(reentry.epoch,epoch:'2020-01-01')&lt(reentry.epoch,epoch:'2021-01-01')",
        'sort': '-reentry.epoch',
    },
)

doc = response.json()

if response.ok:
    print('The query was successful')
    pprint(doc['data'])
    1 / 0
else:
    print('The query failed')
    pprint(doc['errors'])
