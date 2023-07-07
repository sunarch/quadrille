#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

""" regex """

# imports: library
import re


class Regex:
    """ Regex """

    @staticmethod
    def _match(s_to_check, o_compiled_pattern):
        """ _match """

        return_value = None

        match = o_compiled_pattern.fullmatch(s_to_check)

        if match:
            return_value = match.groupdict()

        return return_value

    # rule CLA

    _REGEX_RULE_CLA = re.compile("^rule=(?P<value>((45|90|270|315)-){4}(45|90|270|315))")

    @classmethod
    def parse_cla_rule(cls, s_to_check):
        return cls._match(s_to_check, cls._REGEX_RULE_CLA)

    # speedup CLA

    _REGEX_SPEEDUP_CLA = re.compile("^speedup=(?P<value>[1-9][0-9]*)")

    @classmethod
    def parse_cla_speedup(cls, s_to_check):
        return cls._match(s_to_check, cls._REGEX_SPEEDUP_CLA)

    # color (any)

    _REGEX_COLOR_ANY = re.compile("(?P<color>[0-4])")

    @classmethod
    def parse_color_any(cls, s_to_check):
        return cls._match(s_to_check, cls._REGEX_COLOR_ANY)

    # obstacle

    _REGEX_OBSTACLE = re.compile("(?P<symbol>\\*)")

    @classmethod
    def parse_obstacle(cls, s_to_check):
        return cls._match(s_to_check, cls._REGEX_OBSTACLE)

    # coordinated

    _REGEX_COORDINATES = re.compile("(?P<row>0|[1-9][0-9]*),(?P<column>0|[1-9][0-9]*)")

    @classmethod
    def parse_coordinates(cls, s_to_check):
        return cls._match(s_to_check, cls._REGEX_COORDINATES)

    # count

    _REGEX_COUNT = re.compile("(?P<count>([0-9]|[1-9][0-9]*))")

    @classmethod
    def parse_count(cls, s_to_check):
        return cls._match(s_to_check, cls._REGEX_COUNT)

    # ant (any)

    _REGEX_ANT_ANY = re.compile("(?P<name>[a-zA-Z])")

    @classmethod
    def parse_ant_any(cls, s_to_check):
        return cls._match(s_to_check, cls._REGEX_ANT_ANY)

    # ant data

    _REGEX_ANT_DATA = re.compile("(?P<name>[a-zA-Z]),(?P<row>(0|[1-9][0-9]*)),(?P<column>(0|[1-9][0-9]*))")

    @classmethod
    def parse_ant_data(cls, s_to_check):
        return cls._match(s_to_check, cls._REGEX_ANT_DATA)

    # ant direction

    _REGEX_ANT_DIRECTION = re.compile("((?P<North>[A-Z])|(?P<South>[a-z]))")

    @classmethod
    def parse_ant_direction(cls, s_to_check):
        return cls._match(s_to_check, cls._REGEX_ANT_DIRECTION)

    # ant type

    _REGEX_ANT_TYPE = re.compile("((?P<standard>[a-h])|(?P<busy>[i-q])|(?P<lazy>[r-z]))")

    @classmethod
    def parse_ant_type(cls, s_to_check):
        return cls._match(s_to_check, cls._REGEX_ANT_TYPE)
