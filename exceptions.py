# -*- coding: utf-8 -*-

class InvalidParameter(ValueError):
    """
    Raised for required options that can't be read from CLI arguments or
    configuration file.
    """
    pass
