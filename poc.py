# -*- coding: utf-8 -*-
"""
Read sensor data from the Public NetAtmo API, tag it with a price and attach it
as transaction to the Tangle.
"""
import json

from iota import Iota
from netatmo import APIClient, get_sensor_options
from sender import get_iota_options, attach_tagged_data
from cli import configure_argument_parser


def main(iota_options, sensor_options):
    # configure NetAtmo API client
    sensor_api = APIClient(sensor_options.client_id,
                           sensor_options.client_secret,
                           sensor_options.username,
                           sensor_options.password)
    # configure IOTA API client
    iota_api = Iota(iota_options.node,
                    iota_options.seed.encode('ascii'))
    # get NetAtmo data
    netatmo_query = {
        'lat_ne': 3,
        'lon_ne': 4,
        'lat_sw': -2,
        'lon_sw': -2,
        'filter': True,
        'required_data': 'temperature'
    }
    sensor_data = sensor_api.get_public_data(netatmo_query)
    # tag the transaction with the configured price
    transaction_data = { 'price': iota_options.price, 'data': sensor_data }
    # encode data and attach it to the IOTA tangle
    attach_tagged_data(iota_api,
                       iota_options.address,
                       json.dumps(transaction_data).encode('ascii'),
                       iota_options.tag)

if __name__ == '__main__':
    parser = configure_argument_parser(__doc__, ['iota', 'sensor'])
    cli_args = parser.parse_args()
    sensor_options = get_sensor_options(cli_args)
    iota_options = get_iota_options(cli_args)
    main(iota_options, sensor_options)
