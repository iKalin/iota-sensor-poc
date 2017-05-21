# coding=utf-8
from collections import namedtuple
from subprocess import PIPE, run

import filters as f
from six import binary_type, text_type
from iota import TransactionTrytes
from iota.filters import Trytes

from .cli import read_configuration_file


MAMOptions = namedtuple(
    'MAMOptions', ['start', 'count', 'channel_key_index', 'security_level',
                   'mam_encrypt_path'])


def validate_mam_options(options):
    if options.mam_encrypt_path is None:
        return ('Couldn\'t find a suitable path for the mam encryption '
                'executable to encrypt the message. '
                'Please specify it via the `--mam-encrypt-path` option or set'
                ' the `mam_encrypt_path` variable in your configuration file.')


def get_mam_options(arguments):
    """ """
    file_config = {}
    if arguments.config is not None:
        file_config = read_configuration_file(arguments.config, 'mam')

    options = MAMOptions(
        start=arguments.start or file_config.getint('start'),
        count=arguments.count or file_config.getint('count'),
        channel_key_index=arguments.channel_key_index or file_config.getint('channel_key_index'),
        security_level=arguments.security_level or file_config.getint('security_level'),
        mam_encrypt_path=arguments.mam_encrypt_path or file_config.get('mam_encrypt_path'),
    )

    error = validate_mam_options(options)
    if error:
        raise InvalidParameter(error)

    return options


def encrypt_message(message, iota_api, mam_options):
    """
    TODO: Currently MAM functionality is not implemented in the IOTA Python
    library so we rely on the JS implementation for this POC.

    Uses the specified script at mam_encrypt_path to encrypt the message.
    Returns a list of transaction_trytes or None if there was an issue
    encrypting the message. Mostly taken from [0].

    [0] https://github.com/iotaledger/iota.lib.py/blob/develop/examples/mam_js_send.py
    """

    proc =\
        run(
            args = [
            # mam_encrypt.js
            mam_options.mam_encrypt_path,

            # Required arguments
            binary_type(iota_api.seed),
            message,

            # Options
            '--channel-key-index', text_type(mam_options.channel_key_index),
            '--start', text_type(mam_options.start),
            '--count', text_type(mam_options.count),
            '--security-level', text_type(mam_options.security_level),
            ],

            check   = True,
            stdout  = PIPE,
    )

    filter_ =\
        f.FilterRunner(
            starting_filter =
                f.Required
            | f.Unicode
            | f.JsonDecode
            | f.Array
            | f.FilterRepeater(
                    f.ByteString(encoding='ascii')
                | Trytes(result_type=TransactionTrytes)
                ),

            incoming_data = proc.stdout,
    )

    if not filter_.is_valid():
        return

    return filter_.cleaned_data
