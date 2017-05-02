# -*- coding: utf-8 -*-
import hashlib
import json
import os
from datetime import datetime

from six import text_type

from .cli import read_configuration_file
from .exceptions import InvalidParameter


DEFAULT_BUFFER_SIZE = 0


class Buffer:
    """
    Hold retrieved NetAtmo transactions in a buffer directory until we're ready
    to send them as a single chunk.
    """

    def __init__(self, directory, size):
        self.directory = directory
        self.size = size
        try:
            os.mkdir(self.directory)
        except FileExistsError:
            pass

    def add(self, data):
        """ Add data to buffer. """
        content_hash = hashlib.sha1(data).hexdigest()
        now = datetime.utcnow().timestamp()
        file_name = '{}_{}'.format(now, content_hash)
        with open(os.path.join(self.directory, file_name), 'wb') as fh:
            fh.write(data)

    def read(self):
        """
        Read each item of the buffer into a list. It's assumed buffer files
        contain valid JSON.
        """
        data = []
        for root, subdirs, files in os.walk(self.directory):
            for file_path in files:
                with open(os.path.join(root, file_path), 'r') as fh:
                    data.append(json.loads(fh.read()))
        return data

    def clear(self):
        """ Remove all files from the buffer `directory`. """
        for root, subdirs, files in os.walk(self.directory):
            for file_path in files:
                os.remove(os.path.join(root, file_path))

    @property
    def is_ready(self):
        buffered_files = os.listdir(self.directory)
        return len(buffered_files) >= self.size

    @classmethod
    def from_arguments(cls, arguments):
        file_config = {}
        if arguments.config is not None:
            file_config = read_configuration_file(arguments.config, 'buffer')

        size = arguments.buffer_size
        if size is None:
            if 'size' in file_config:
                size = file_config.getint('size')
            else:
                size = DEFAULT_BUFFER_SIZE
        directory = arguments.buffer_directory or file_config.get('directory',
                                                                  None)

        if not isinstance(directory, text_type):
            raise InvalidParameter((
                'Invalid buffer directory. Please specify it via the '
                '--buffer-directory argument or in your configuration '
                'file with the `directory` variable under [buffer].'
            ))

        if not isinstance(size, int) and size >= 0:
            raise InvalidParameter((
                'Invalid buffer size. Please specify a positive integer via '
                'the --buffer-size argument or in your configuration file with'
                ' the `size` variable under [buffer].'
            ))
        return cls(directory, size)
