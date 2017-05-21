# -*- coding: utf-8 -*-
import configparser
import sys
from argparse import ArgumentParser

from six import text_type


def configure_argument_parser(description, namespaces):
    """
    namespaces: 'iota', 'sensor', ['iota', 'sensor']
    """

    if isinstance(namespaces, text_type):
        namespaces = [namespaces]

    parser = ArgumentParser(description=description)
    ArgumentParser()

    parser.add_argument(
        '--config',
        type=text_type,
        help='configuration file to read options from.',
    )

    if 'iota' in namespaces:
        parser.add_argument(
            '--node',
            type=text_type,
            default='http://localhost:14265/',
            help='node to connect to (defaults to http://localhost:14265/).'
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
            '--price',
            type=float,
            help='price value to attach to the data.',
        )

        parser.add_argument(
            '--depth',
            type=int,
            help='Depth at which to attach the resulting transactions.',
        )

        parser.add_argument(
            '--min-weight-magnitude',
            dest='min_weight_magnitude',
            type=int,
            help='Min weight magnitude, used by the node to calibrate PoW.'
        )

    if 'sensor' in namespaces:
        parser.add_argument(
            '--client_id',
            type=text_type,
            help='client_id to used to connect to the NetAtmo API.'
        )

        parser.add_argument(
            '--client_secret',
            type=text_type,
            help='client_secret used to connect to the NetAtmo API.'
        )

        parser.add_argument(
            '--username',
            type=text_type,
            help='username used to connect to the NetAtmo API.'
        )

        parser.add_argument(
            '--password',
            type=text_type,
            help='password used to connect to the NetAtmo API.',
        )

    if 'mam' in namespaces:
        parser.add_argument(
            '--start',
            type=int,
            help='Index of the first key used to encrypt the message.',
        )

        parser.add_argument(
            '--count',
            type=int,
            help='Password used to connect to the NetAtmo API.',
        )

        parser.add_argument(
            '--channel-key-index',
            dest='channel_key_index',
            type=int,
            help='Index of the key used to establish the channel.',
        )

        parser.add_argument(
            '--mam-encrypt-path',
            dest='mam_encrypt_path',
            help='Path to `mam_encrypt.js` script.',
        )

        parser.add_argument(
            '--security_level',
            dest='security_level',
            type=int,
            help='Specifies the security level of your transactions',
        )

    return parser


def read_configuration_file(config_file_path, section):
    """
    Reads section `section` of the configuration file and returns it as a dict.
    """
    if not isinstance(section, text_type):
        raise ValueError('Invalid section name {}'.format(section))

    config = configparser.ConfigParser()
    wrong_header_error = ('Your config file is incorrect. Add a [{}] '
                          'section header to it.'.format(section))
    try:
        with open(config_file_path) as config_file_handle:
            config.read_file(config_file_handle)
    except IOError:
        error = ('There was a problem reading the configuration file "{}". '
                 '(If running as a Snap, make sure you\'re reading from '
                 'your home directory.)')
        sys.exit(error.format(config_file_path))
    except configparser.MissingSectionHeaderError:
        sys.exit(wrong_header_error)
    try:
        return config[section]
    except KeyError:
        sys.exit(wrong_header_error)
