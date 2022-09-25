#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

""" Output styling with ASCII escape sequences
    Version 1.1

    https://en.wikipedia.org/wiki/ANSI_escape_code
"""


class AsciiStyle:
    """ AsciiStyle """

    @staticmethod
    def bold(arg_printable):
        """ bold """
        return "\x1b[1m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def faint(arg_printable):
        """ faint """
        return "\x1b[2m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def italic(arg_printable):
        """ italic """
        return "\x1b[3m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def underlined(arg_printable):
        """ underlined """
        return "\x1b[4m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def blink(arg_printable):
        """ blink """
        return "\x1b[5m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def image_negative(arg_printable):
        """ image_negative """
        return "\x1b[7m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def framed(arg_printable):
        """ framed """
        return "\x1b[51m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def encircled(arg_printable):
        """ encircled """
        return "\x1b[52m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def overlined(arg_printable):
        """ overlined """
        return "\x1b[53m{0}\x1b[0m".format(arg_printable)


class AsciiFont:
    """ AsciiFont """

    @staticmethod
    def primary(arg_printable):
        """ primary """
        return "\x1b[10m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def alternate(arg_printable, arg_alternate_font_no):
        """ alternate """

        inserted_no = "1"

        if int(arg_alternate_font_no) in range(1, 10):  # 0 < x < 10 #
            inserted_no = str(arg_alternate_font_no)

        return "\x1b[1{0}m{1}\x1b[0m".format(inserted_no, arg_printable)


class AsciiColor:
    """ AsciiColor """

    @staticmethod
    def black(arg_printable):
        """ black """
        return "\x1b[30m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def red(arg_printable):
        """ red """
        return "\x1b[31m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def green(arg_printable):
        """ green """
        return "\x1b[32m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def yellow(arg_printable):
        """ yellow """
        return "\x1b[33m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def blue(arg_printable):
        """ blue """
        return "\x1b[34m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def magenta(arg_printable):
        """ magenta """
        return "\x1b[35m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def cyan(arg_printable):
        """ cyan """
        return "\x1b[36m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def white(arg_printable):
        """ white """
        return "\x1b[37m{0}\x1b[0m".format(arg_printable)


class AsciiBackground:
    """ AsciiBackground """

    @staticmethod
    def black(arg_printable):
        """ black """
        return "\x1b[40m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def red(arg_printable):
        """ red """
        return "\x1b[41m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def green(arg_printable):
        """ green """
        return "\x1b[42m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def yellow(arg_printable):
        """ yellow """
        return "\x1b[43m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def blue(arg_printable):
        """ blue """
        return "\x1b[44m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def magenta(arg_printable):
        """ magenta """
        return "\x1b[45m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def cyan(arg_printable):
        """ cyan """
        return "\x1b[46m{0}\x1b[0m".format(arg_printable)

    @staticmethod
    def white(arg_printable):
        """ white """
        return "\x1b[47m{0}\x1b[0m".format(arg_printable)
