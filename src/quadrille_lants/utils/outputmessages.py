##!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

""" output messages """

# imports: project
from quadrille_lants.utils.asciistyling import AsciiStyle as Sty
from quadrille_lants.utils.asciistyling import AsciiColor as Color


class OutputMessages:
    """ OutputMessages """

    @staticmethod
    def error_details(error):
        """ error_details """
        print("{0}, {1}".format(Sty.bold(Color.red("Error")), error.args[0]))

    @staticmethod
    def error(message):
        """ error """
        print("{0}, {1}".format(Sty.bold(Color.red("Error")), message))

    @staticmethod
    def warning(message):
        """ warning """
        print("{0}, {1}".format(Sty.bold(Color.yellow("Warning")), message))

    @staticmethod
    def info(message):
        """ info """
        print("{0}, {1}".format(Sty.bold(Color.blue("Info")), message))
