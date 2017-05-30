# -*- coding: utf-8 -*-
"""
Send arbitrary data as IOTA transactions.
"""
import sys
from collections import namedtuple
from pprint import pprint

from iota import Iota, BadApiResponse
from requests.exceptions import ConnectionError

from .exceptions import InvalidParameter
from .mam_encryption import encrypt_message


IOTAOptions = namedtuple(
    'IOTAOptions', ['node', 'seed', 'price', 'depth', 'min_weight_magnitude']
)


def get_iota_options(arguments):

    if arguments.node is None:
        raise InvalidParameter(
            ('Couldn\'t find a suitable node to connect to. '
             'Please specify it via the `--node` option or set the `node`'
             ' variable in your configuration file.')
        )

    if arguments.seed is None:
        raise InvalidParameter(
            ('Couldn\'t find a suitable seed to use. '
             'Please specify it via the `--seed` option or set the `seed`'
             ' variable in your configuration file.')
        )

    if arguments.price is None:
        raise InvalidParameter(
            ('Couldn\'t find a suitable price to use. '
             'Please specify it via the `--price` option or set the `price`'
             ' variable in your configuration file.')
        )

    return IOTAOptions(node=arguments.node,
                       seed=arguments.seed,
                       price=arguments.price,
                       depth=arguments.depth,
                       min_weight_magnitude=arguments.min_weight_magnitude)


def attach_encrypted_message(message, iota_options, mam_options):
    iota_api = Iota(iota_options.node, iota_options.seed.encode('ascii'))

    transaction_trytes = encrypt_message(
        message.decode('utf-8'),
        iota_api, mam_options
    )

    if not transaction_trytes:
        raise Exception('Failed to encrypt message.')

    try:
        iota_api.send_trytes(
            trytes=transaction_trytes,
            depth=iota_options.depth,
            min_weight_magnitude=iota_options.min_weight_magnitude,
        )
    except BadApiResponse as e:
        pprint(getattr(e, 'context', {}))
        raise
    return True
