# -*- coding: utf-8 -*-
"""
Read sensor data from the Public NetAtmo API, tag it with a price and attach it
as transaction to the Tangle.
"""
import json
import sys

from six import text_type
from iota import Iota

from .buffer import Buffer
from .cli import configure_argument_parser
from .exceptions import InvalidParameter
from .netatmo import APIClient, get_sensor_options
from .sender import get_iota_options, attach_encrypted_message
from .mam_encryption import get_mam_options


def main():

    parser = configure_argument_parser(__doc__)
    args = parser.parse_args()
    try:
        file_buffer = Buffer.from_arguments(args)
        sensor_options = get_sensor_options(args)
        iota_options = get_iota_options(args)
        mam_options = get_mam_options(args)
    except InvalidParameter as e:
        sys.exit(e)

    # configure NetAtmo API client
    sensor_api = APIClient(sensor_options.client_id,
                           sensor_options.client_secret,
                           sensor_options.username,
                           sensor_options.password)
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

    file_buffer.add(json.dumps(sensor_data).encode('ascii'))
    if not file_buffer.is_ready:
        return
    sensor_data = file_buffer.read()

    # tag the transaction with the configured price
    transaction_data = json.dumps({
        'price': iota_options.price,
        'data': sensor_data
    }).encode('ascii')

    # encode data and attach it to the IOTA tangle
    attach_encrypted_message(
        transaction_data,
        iota_options,
        mam_options,
    )

    file_buffer.clear()

if __name__ == '__main__':
    main()
