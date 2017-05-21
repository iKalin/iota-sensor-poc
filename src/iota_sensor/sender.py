# -*- coding: utf-8 -*-
"""
Send arbitrary data as IOTA transactions.
"""
import sys
from collections import namedtuple
from pprint import pprint

from iota import Iota, BadApiResponse
from requests.exceptions import ConnectionError
from six import text_type

from .cli import read_configuration_file, configure_argument_parser
from .exceptions import InvalidParameter
from .mam_encryption import encrypt_message, get_mam_options


DEFAULT_PRICE = 0.0


IOTAOptions = namedtuple(
    'IOTAOptions', ['node', 'seed', 'address', 'tag', 'price', 'depth',
                    'min_weight_magnitude']
)


def validate_iota_options(options):
    if options.node is None:
        return ('Couldn\'t find a suitable node to connect to. '
                'Please specify it via the `--node` option or set the `node`'
                ' variable in your configuration file.')

    if options.seed is None:
        return ('Couldn\'t find a suitable seed to use. '
                'Please specify it via the `--seed` option or set the `seed`'
                ' variable in your configuration file.')

    if options.price is None:
        return ('Couldn\'t find a suitable price to use. '
                'Please specify it via the `--price` option or set the `price`'
                ' variable in your configuration file.')

    if options.address is None:
        return ('Couldn\'t find a suitable address to send the transaction '
                'to. Please specify it via the `--address` option or set '
                'the `address` variable in your configuration file.')

    if options.tag is None:
        return ('Couldn\'t find a suitable ID to tag the message with. '
                'Please specify it via the `--tag` option or set the `tag`'
                ' variable in your configuration file.')


def get_iota_options(arguments):
    """
    Parse options from both the CLI and config file if specified.
    """
    file_config = {}
    if arguments.config is not None:
        file_config = read_configuration_file(arguments.config, 'iota')

    price = arguments.price
    if price is None:
        if 'price' in file_config:
            price = file_config.getfloat('price')
        else:
            price = DEFAULT_PRICE

    options = IOTAOptions(
        node=arguments.node or file_config.get('node'),
        seed=arguments.seed or file_config.get('seed'),
        address=arguments.address or file_config.get('address'),
        tag=arguments.tag or file_config.get('tag'),
        price=price,
        depth=arguments.depth or file_config.getint('depth'),
        min_weight_magnitude=arguments.min_weight_magnitude or file_config.getint('min_weight_magnitude'),
    )

    error = validate_iota_options(options)
    if error:
        raise InvalidParameter(error)

    return options


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


def main(iota_options, mam_options, data=None, data_file=None):
    try:
        api = Iota(iota_options.node, iota_options.seed.encode('ascii'))
    except ValueError:
        sys.exit('The provided seed value is invalid.')

    if data:
        data = data.encode('ascii')
    elif data_file:
        print('Reading data file "{}"...'.format(data_file))
        try:
            with open(data_file, 'rb') as input_file_handle:
                data = input_file_handle.read()
        except IOError:
            sys.exit('Couldn\'t read data file "{}"'.format(data_file))
    else:
        data = sys.stdin.read()

    attach_encrypted_message(data, iota_options, mam_options)


if __name__ == '__main__':
    parser = configure_argument_parser(__doc__, ['iota', 'mam'])

    parser.add_argument(
        '--data',
        type=text_type,
        help='data to send as part of the transaction(s).',
    )

    parser.add_argument(
        '--file',
        type=text_type,
        help='file to read data from.',
    )

    parser.add_argument(
        '--stdin',
        help='whether to read data from stdin.',
        action="store_true"
    )

    arguments = parser.parse_args()
    iota_options = get_iota_options(arguments)
    mam_options = get_mam_options(arguments)

    if not arguments.data and not arguments.file and not arguments.stdin:
        sys.exit(('At least one of `--data`, `--file` or `--stdin` needs to '
                  'be specified to read the message from.'))

    main(iota_options, mam_options, arguments.data, arguments.file)
