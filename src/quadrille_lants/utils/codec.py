##!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

""" codec """

# imports: library
import hashlib


# object encode / decode

class ObjectCodec:
    """ ObjectCodec """

    @staticmethod
    def encode(arg_object):
        """ encode """
        return arg_object.encode('utf-8')

    @staticmethod
    def decode(arg_object):
        """ decode """
        return arg_object.decode('utf-8')


# hashing

class Hashing:
    """ Hashing """

    @staticmethod
    def hash_sha1(arg_object):
        """ hash_sha1 """
        return hashlib.sha1(arg_object).hexdigest()

    @staticmethod
    def integer_hash(arg_hex_digest):
        """ integer_hash """
        return int(arg_hex_digest[:8], 16)  # 8 hex digits of precision
