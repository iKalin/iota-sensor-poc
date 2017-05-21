# -*- coding: utf-8 -*-
"""
Read data from NetAtmo's public API.
"""
from collections import namedtuple

import requests

from .exceptions import InvalidParameter


SensorAPIOptions = namedtuple(
    'SensorAPIOptions',
    ['client_id', 'client_secret', 'username', 'password']
)


def get_sensor_options(arguments):

    if arguments.client_id is None:
        raise InvalidParameter(
            ('Couldn\'t find a suitable `client_id` to connect to the '
             'NetAtmo API. Please specify it via the `--client_id` '
             'option or set the `client_id` variable under the [sensor]'
             ' section of your configuration file.')
        )

    if arguments.client_secret is None:
        raise InvalidParameter(
            ('Couldn\'t find a suitable `client_secret` to connect to the '
             'NetAtmo API. Please specify it via the `--client_secret` '
             'option or set the `client_secret` variable under the [sensor]'
             ' section of your configuration file.')
        )

    if arguments.username is None:
        raise InvalidParameter(
            ('Couldn\'t find a suitable `username` to connect to the '
             'NetAtmo API. Please specify it via the `--username` '
             'option or set the `username` variable under the [sensor]'
             ' section of your configuration file.')
        )

    if arguments.password is None:
        raise InvalidParameter(
            ('Couldn\'t find a suitable `password` to connect to the '
             'NetAtmo API. Please specify it via the `--password` '
             'option or set the `password` variable under the [sensor]'
             ' section of your configuration file.')
        )

    return SensorAPIOptions(client_id=arguments.client_id,
                            client_secret=arguments.client_secret,
                            username=arguments.username,
                            password=arguments.password)


class APIClient:

    base_url = 'https://api.netatmo.com/'

    def __init__(self, client_id, client_secret, username, password):
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.access_token = None
        self.refresh_token = None

    def get_access_token(self, scope='read_station', grant_type='password'):
        url = self.base_url + 'oauth2/token'

        data = {'client_id': self.client_id,
                'client_secret': self.client_secret,
                'username': self.username,
                'password': self.password,
                'scope': scope,
                'grant_type': grant_type}
        headers = {'Content-Type': 'application/x-www-form-urlencoded;'}

        response = requests.post(url, data=data, headers=headers)

        if response.status_code != 200:
            raise IOError(response.json())
        parsed_response = response.json()
        self.access_token = parsed_response['access_token']
        self.refresh_token = parsed_response['refresh_token']
        self.access_token_expiry = parsed_response['expires_in']

    def get_public_data(self, query):

        url = self.base_url + 'api/getpublicdata'

        if self.access_token is None:
            self.get_access_token()

        data = dict(query)
        data['access_token'] = self.access_token
        response = requests.get(url, data)

        if response.status_code != 200:
            raise IOError(response.json())
        return response.json()
