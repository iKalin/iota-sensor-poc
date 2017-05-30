# -*- coding: utf-8 -*-
import argparse
import configparser


class ConfigurationFileArgumentParser(argparse.ArgumentParser):
    """
    ArgumentParser extension that reads from a configuration file when no
    options is supplied.

    The precedence of the options is as follows:

    - Use directly specified option
    - Use option read from configuration file
    - Use `default` value from `add_argument`

    Adds a `config_file_section` keyword argument to `add_argument` to specify
    the section of the configuration file where we want to make the lookup.
    """

    _registered_arguments = []

    def __init__(self, *args, **kwargs):
        self.config_file_option_name = kwargs.pop(
            'config_file_option_name',
            None
        )
        if not isinstance(self.config_file_option_name, str):
            raise TypeError(('{} initializer requires a keyword argument '
                             '"config_file_option_name"').format(
                                 self.__class__.__name__))
        super().__init__(*args, **kwargs)
        super().add_argument(
            '--{}'.format(self.config_file_option_name),
            type=str,
            help='Configuration file to read options from.',
        )

    def add_argument(self, *args, **kwargs):
        section = kwargs.pop('config_file_section', None)
        default = kwargs.pop('default', None)
        action = super().add_argument(*args, **kwargs)
        self._registered_arguments.append((action, section, default))
        return action

    def _read_configuration_file(self, config_file_path):
        config = configparser.ConfigParser()
        with open(config_file_path) as config_file_handle:
            config.read_file(config_file_handle)
        return config

    def parse_args(self, *args, **kwargs):
        args = super().parse_args(*args, **kwargs)

        configuration_file = getattr(args, self.config_file_option_name, None)
        if configuration_file:
            try:
                file_config = self._read_configuration_file(configuration_file)
            except IOError:
                self.error('\nThere was a problem reading the configuration '
                           'file "{}". \n(If running as a Snap, make sure '
                           'you\'re reading from your home directory.)')
        else:
            file_config = {}

        for (action, section, default) in self._registered_arguments:

            if isinstance(action, argparse._HelpAction):
                continue
            if action.dest == self.config_file_option_name:
                continue

            argument_name = action.dest
            value = getattr(args, argument_name)

            # read from configuration file
            if value is None and section in file_config:
                value = file_config.get(section, argument_name, fallback=None)

            # use default valye
            if value is None:
                value = default

            # try to convert the value to the required type
            if isinstance(value, str):
                try:
                    value = self._get_value(action, value)
                except Exception as e:
                    self.error(argparse.ArgumentError(action, e.message))

            setattr(args, argument_name, value)
        return args


def configure_argument_parser(description):

    parser = ConfigurationFileArgumentParser(
        description=description,
        config_file_option_name='config'
    )

    ##############
    # IOTA section
    ##############
    parser.add_argument(
        '--node',
        type=str,
        default='http://localhost:14265/',
        config_file_section='iota',
        help='node to connect to (defaults to http://localhost:14265/).'
    )

    parser.add_argument(
        '--seed',
        type=str,
        config_file_section='iota',
        help='seed to use.',
    )

    parser.add_argument(
        '--price',
        type=float,
        default=0.0,
        config_file_section='iota',
        help='price value to attach to the data.',
    )

    parser.add_argument(
        '--depth',
        type=int,
        config_file_section='iota',
        help='Depth at which to attach the resulting transactions.',
    )

    parser.add_argument(
        '--min-weight-magnitude',
        dest='min_weight_magnitude',
        type=int,
        config_file_section='iota',
        help='Min weight magnitude, used by the node to calibrate PoW.'
    )

    ################
    # sensor section
    ################
    parser.add_argument(
        '--client_id',
        type=str,
        config_file_section='sensor',
        help='client_id to used to connect to the NetAtmo API.'
    )

    parser.add_argument(
        '--client_secret',
        type=str,
        config_file_section='sensor',
        help='client_secret used to connect to the NetAtmo API.'
    )

    parser.add_argument(
        '--username',
        type=str,
        config_file_section='sensor',
        help='username used to connect to the NetAtmo API.'
    )

    parser.add_argument(
        '--password',
        type=str,
        config_file_section='sensor',
        help='password used to connect to the NetAtmo API.',
    )

    #############
    # mam section
    #############
    parser.add_argument(
        '--start',
        type=int,
        config_file_section='mam',
        help='Index of the first key used to encrypt the message.',
    )

    parser.add_argument(
        '--count',
        type=int,
        config_file_section='mam',
        help='Password used to connect to the NetAtmo API.',
    )

    parser.add_argument(
        '--channel-key-index',
        dest='channel_key_index',
        type=int,
        config_file_section='mam',
        help='Index of the key used to establish the channel.',
    )

    parser.add_argument(
        '--mam-encrypt-path',
        dest='mam_encrypt_path',
        config_file_section='mam',
        help='Path to `mam_encrypt.js` script.',
    )

    parser.add_argument(
        '--security_level',
        dest='security_level',
        type=int,
        config_file_section='mam',
        help='Specifies the security level of your transactions',
    )

    ################
    # buffer section
    ################
    parser.add_argument(
        '--buffer-size',
        help=('how many NetAtmo responses to store locally before attaching '
              'them to the Tangle (defaults to 0)'),
        type=int,
        default=0,
        config_file_section='buffer',
    )
    parser.add_argument(
        '--buffer-directory',
        type=str,
        help=(('directory to store NetAtmo responses before attaching them as'
               ' a single chunk.')),
        config_file_section='buffer',
    )

    return parser
