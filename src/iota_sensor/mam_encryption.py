# coding=utf-8
from collections import namedtuple
from subprocess import PIPE, run

import filters as f
from six import binary_type, text_type
from iota import TransactionTrytes
from iota.filters import Trytes

from .exceptions import InvalidParameter


MAMOptions = namedtuple(
    'MAMOptions', ['start', 'count', 'channel_key_index', 'security_level',
                   'mam_encrypt_path'])


def get_mam_options(arguments):
    if arguments.mam_encrypt_path is None:
        raise InvalidParameter(
            ('Couldn\'t find a suitable path for the mam encryption '
             'executable to encrypt the message. '
             'Please specify it via the `--mam-encrypt-path` option or set'
             ' the `mam_encrypt_path` variable in your configuration file.')
        )

    return MAMOptions(start=arguments.start,
                      count=arguments.count,
                      channel_key_index=arguments.channel_key_index,
                      security_level=arguments.security_level,
                      mam_encrypt_path=arguments.mam_encrypt_path)


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
