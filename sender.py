# -*- coding: utf-8 -*-
"""
Script to send arbitrary data as IOTA transactions.
"""
import configparser
import sys

from argparse import ArgumentParser
from collections import namedtuple
from six import text_type

from iota import Iota, Address, TryteString, ProposedTransaction
from requests.exceptions import ConnectionError


Options = namedtuple('Options', ['node', 'seed', 'address', 'tag', 'data', 'file'])


def read_configuration_file(config_file_path):
    """ """
    config = configparser.ConfigParser()
    wrong_header_error = ('Your config file is incorrect. Add a [default] '
                          'section header to it.')
    try:
        with open(config_file_path) as config_file_handle:
            config.read_file(config_file_handle)
    except IOError:
        error = 'There was a problem reading the configuration file "{}"'
        sys.exit(error.format(config_file_path))
    except configparser.MissingSectionHeaderError:
        sys.exit(wrong_header_error)
    try:
        return config['default']
    except KeyError:
        sys.exit(wrong_header_error)


def get_options(arguments):
    """
    Parse options from both the CLI and config file if specified.
    """
    file_config = {}
    if arguments.config is not None:
        file_config = read_configuration_file(arguments.config)

    options = Options(
        node=arguments.node or file_config.get('node'),
        seed=arguments.seed or file_config.get('seed'),
        address=arguments.address or file_config.get('address'),
        tag=arguments.tag or file_config.get('tag'),
        data=arguments.data,
        file=arguments.file
    )

    if not arguments.data and not arguments.file and not arguments.stdin:
        sys.exit(('At least one of `--data`, `--file` or `--stdin` needs to '
                  'be specified to read the message from.'))

    if options.node is None:
        sys.exit(('Couldn\'t find a suitable node to connect to. '
                  'Please specify it via the `--node` option or set the `node`'
                  ' variable in your configuration file.'))

    if options.seed is None:
        sys.exit(('Couldn\'t find a suitable seed to use. '
                  'Please specify it via the `--seed` option or set the `seed`'
                  ' variable in your configuration file.'))

    if options.address is None:
        sys.exit(('Couldn\'t find a suitable address to send the transaction '
                  'to. Please specify it via the `--address` option or set '
                  'the `address` variable in your configuration file.'))

    if options.tag is None:
        sys.exit(('Couldn\'t find a suitable ID to tag the message with. '
                  'Please specify it via the `--tag` option or set the `tag`'
                  ' variable in your configuration file.'))

    return options


def send_tagged_message(api, address, data, tag):
    """ """
    address = Address(address.encode('ascii'))
    tag = TryteString.from_string(tag)
    message = TryteString.from_bytes(data.encode('ascii'))
    transaction = ProposedTransaction(address, 0, tag=tag, message=message)
    transfer_response = api.send_transfer(9, [transaction])


def main(options):
    try:
        api = Iota(options.node, options.seed.encode('ascii'))
    except ValueError:
        sys.exit('The provided seed value is invalid.')

    if options.data:
        data = options.data
    elif options.file:
        print('Reading data file "{}"...'.format(options.file))
        try:
            with open(options.file, 'rb') as input_file_handle:
                data = input_file_handle.read()
        except IOError:
            sys.exit('Couldn\'t read data file "{}"'.format(options.file))
    else:
        data = sys.stdin.read()

    try:
        send_tagged_message(api, options.address, data, options.tag)
    except ConnectionError as e:
        print(e)
        sys.exit('Couldn\'t connect to node "{}".'.format(options.node))


if __name__ == '__main__':
    parser = ArgumentParser(description = __doc__)

    parser.add_argument(
      '--node',
      type    = text_type,
      default = 'http://localhost:14265/',
      help = 'node to connect to (defaults to http://localhost:14265/).'
    )

    parser.add_argument(
        '--seed',
        type=text_type,
        help='seed to use.',
    )

    parser.add_argument(
        '--address',
        type=text_type,
        help='address to send the data to.',
    )

    parser.add_argument(
        '--tag',
        type=text_type,
        help='identifying Tag for the stream',
    )

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
        '--config',
        type=text_type,
        help='configuration file to read options from.',
    )

    parser.add_argument(
        '--stdin',
        help='whether to read data from stdin.',
        action="store_true"
    )

    options = get_options(parser.parse_args())
    main(options)
