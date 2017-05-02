# -*- coding: utf-8 -*-
"""
Send arbitrary data as IOTA transactions.
"""
import sys
from collections import namedtuple

from iota import Iota, Address, TryteString, ProposedTransaction
from requests.exceptions import ConnectionError
from six import text_type

from .cli import read_configuration_file, configure_argument_parser
from .exceptions import InvalidParameter


IOTAOptions = namedtuple(
    'Options',
    ['node', 'seed', 'address', 'tag', 'price']
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

    options = IOTAOptions(
        node=arguments.node or file_config.get('node'),
        seed=arguments.seed or file_config.get('seed'),
        address=arguments.address or file_config.get('address'),
        tag=arguments.tag or file_config.get('tag'),
        price=arguments.tag or file_config.getfloat('price')
    )

    error = validate_iota_options(options)
    if error:
        raise InvalidParameter(error)

    return options


def attach_tagged_data(api, address, data, tag):
    """ """
    address = Address(address.encode('ascii'))
    tag = TryteString.from_string(tag)
    message = TryteString.from_bytes(data)
    transaction = ProposedTransaction(address, 0, tag=tag, message=message)
    try:
        transfer_response = api.send_transfer(9, [transaction])
    except ConnectionError:
        raise IOError('Couldn\'t connect to node.')


def main(options, data=None, data_file=None):
    try:
        api = Iota(options.node, options.seed.encode('ascii'))
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

    attach_tagged_data(api, options.address, data, options.tag)


if __name__ == '__main__':
    parser = configure_argument_parser(__doc__, 'iota')

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
    options = get_iota_options(arguments)

    if not arguments.data and not arguments.file and not arguments.stdin:
        sys.exit(('At least one of `--data`, `--file` or `--stdin` needs to '
                  'be specified to read the message from.'))

    main(options, arguments.data, arguments.file)
