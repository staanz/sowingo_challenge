# -*- coding: utf-8 -*-

"""Helper utilies which deal with UUID generation.

:copyright: (c) 2020 by Sowingo.com Corp.
"""

import shortuuid

__all__ = [
    'uuid_with_prefix'
]

def uuid_with_prefix(prefix=None):
    """A helper utility to allow a prefix to be attached when generating
    UUIDs.

    :param:`prefix` - A string which must be prefixed to the generated UUID.
    :return:`UUID` - The generated UUID (with a prefix, if applicable).
    """
    return shortuuid.uuid() if not prefix \
        else prefix + shortuuid.uuid()
