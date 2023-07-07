#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

""" ant """

# imports: project
from quadrille_lants.utils.regex import Regex
from quadrille_lants.utils.codec import ObjectCodec as Codec
from quadrille_lants.utils.codec import Hashing as Hashing


# An ant #

class Ant:
    """ Ant """

    # Orientations #
    ORIENTATION_NORTH = "N"
    ORIENTATION_NORTHEAST = "NE"
    ORIENTATION_EAST = "E"
    ORIENTATION_SOUTHEAST = "SE"
    ORIENTATION_SOUTH = "S"
    ORIENTATION_SOUTHWEST = "SW"
    ORIENTATION_WEST = "W"
    ORIENTATION_NORTHWEST = "NW"

    ORIENTATION_TO_STR_DICT = {
        0:   ORIENTATION_NORTH,
        45:  ORIENTATION_NORTHEAST,
        90:  ORIENTATION_EAST,
        135: ORIENTATION_SOUTHEAST,
        180: ORIENTATION_SOUTH,
        225: ORIENTATION_SOUTHWEST,
        270: ORIENTATION_WEST,
        315: ORIENTATION_NORTHWEST
    }

    # ant directional target meta values #
    ONENORTH = -1
    ONEWEST = -1
    INPLACE = 0
    ONESOUTH = 1
    ONEEAST = 1

    def __init__(self, arg_ant_name, arg_pos_row, arg_pos_column):

        self.name = None
        self.orientation = None

        parsed = Regex.parse_ant_direction(arg_ant_name)

        if parsed is not None:
            if parsed["North"] is not None:
                self.name = parsed["North"].lower()
                self.orientation = 0
            elif parsed["South"] is not None:
                self.name = parsed["South"].lower()
                self.orientation = 180

        self.hash = Hashing.integer_hash(Hashing.hash_sha1(Codec.encode(self.get_name())))
        self.ant_type = None  # "standard" ant, "busy" ant, "lazy" ant #

        parsed = Regex.parse_ant_type(self.get_name())

        if parsed is not None:
            if parsed["standard"] is not None:
                self.ant_type = "standard"
            elif parsed["busy"] is not None:
                self.ant_type = "busy"
            elif parsed["lazy"] is not None:
                self.ant_type = "lazy"

        self.pos_row = -1
        self.pos_column = -1
        self.set_position(arg_pos_row, arg_pos_column)

        self.target_pos_row_relation = 0
        self.target_pos_column_relation = 0

    def __lt__(self, other):
        return self.get_name() < other.get_name()

    def __le__(self, other):
        return self.get_name() <= other.get_name()

    def __eq__(self, other):
        return self.get_name() == other.get_name()

    def __ne__(self, other):
        return self.get_name() != other.get_name()

    def __gt__(self, other):
        return self.get_name() > other.get_name()

    def __ge__(self, other):
        return self.get_name() >= other.get_name()

    def __hash__(self):
        return self.get_hash()

    def get_name(self):
        """ get_name """
        return self.name

    def get_hash(self):
        """ get_hash """
        return self.hash

    def get_orientation_str(self):
        """ get_orientation_str """
        return self.ORIENTATION_TO_STR_DICT[self.orientation]

    def change_orientation(self, arg_angle):
        """ change_orientation """
        self.orientation = (self.orientation + arg_angle) % 360

    def get_target_pos_row_relation(self):
        """ get_target_pos_row_relation """
        return self.target_pos_row_relation

    def get_target_pos_column_relation(self):
        """ get_target_pos_column_relation """
        return self.target_pos_column_relation

    def set_targat_pos_relation(self, arg_target_pos_row_relation, arg_target_pos_column_relation):
        """ set_targat_pos_relation """
        self.target_pos_row_relation = arg_target_pos_row_relation
        self.target_pos_column_relation = arg_target_pos_column_relation

    def get_type(self):
        """ get_type """
        return self.ant_type

    def get_position_str(self):
        """ get_position_str """
        return str(self.pos_row) + "," + str(self.pos_column)

    def get_pos_row(self):
        """ get_pos_row """
        return self.pos_row

    def get_pos_column(self):
        """ get_pos_column """
        return self.pos_column

    def set_position(self, arg_pos_row, arg_pos_column):
        """ set_position """
        self.pos_row = arg_pos_row
        self.pos_column = arg_pos_column

    def calc_target_row_n_col(self):

        orientation_str = self.get_orientation_str()

        if orientation_str == self.ORIENTATION_NORTH:
            self.set_targat_pos_relation(self.ONENORTH, self.INPLACE)
        elif orientation_str == self.ORIENTATION_NORTHEAST:
            self.set_targat_pos_relation(self.ONENORTH, self.ONEEAST)
        elif orientation_str == self.ORIENTATION_EAST:
            self.set_targat_pos_relation(self.INPLACE, self.ONEEAST)
        elif orientation_str == self.ORIENTATION_SOUTHEAST:
            self.set_targat_pos_relation(self.ONESOUTH, self.ONEEAST)
        elif orientation_str == self.ORIENTATION_SOUTH:
            self.set_targat_pos_relation(self.ONESOUTH, self.INPLACE)
        elif orientation_str == self.ORIENTATION_SOUTHWEST:
            self.set_targat_pos_relation(self.ONESOUTH, self.ONEWEST)
        elif orientation_str == self.ORIENTATION_WEST:
            self.set_targat_pos_relation(self.INPLACE, self.ONEWEST)
        elif orientation_str == self.ORIENTATION_NORTHWEST:
            self.set_targat_pos_relation(self.ONENORTH, self.ONEWEST)

        target_row = self.pos_row + self.target_pos_row_relation
        target_col = self.pos_column + self.target_pos_column_relation

        return target_row, target_col
