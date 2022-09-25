#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

""" cell """

# imports: library
import random

# imports: project
from quadrille_lants.utils.outputmessages import OutputMessages as Msg
from quadrille_lants.utils.asciistyling import AsciiStyle as Sty
from quadrille_lants.utils.asciistyling import AsciiColor as Color
from quadrille_lants.utils.asciistyling import AsciiBackground as Bg


class Cell:
    """ A cell on the game grid """

    OBSTACLE_COLOR = -1
    MIN_COLOR_INDEX = 0
    MAX_COLOR_INDEX = 4
    DEFAULT_COLOR = 0

    def __init__(self, arg_type):
        self.color = -1  # default value is obstacle #
        self.occupying_ant = None

        if arg_type >= 0:
            self.set_color(arg_type)

    def has_occupying_ant(self):
        """ has_occupying_ant """
        # return False if None, True if set
        return bool(self.occupying_ant)

    def get_occupying_ant(self):
        """ get_occupying_ant """
        return self.occupying_ant

    def set_occupying_ant(self, new_occupying_ant):
        """ set_occupying_ant """
        self.occupying_ant = new_occupying_ant

    def remove_occupying_ant(self):
        """ remove_occupying_ant """
        self.occupying_ant = None

    def is_obstacle(self):
        """ is_obstacle """
        # return False of True
        return bool(self.color < 0)

    def make_obstacle(self):
        """ make_obstacle """
        self.color = self.OBSTACLE_COLOR

    def get_color(self):
        """ get_color """
        return self.color

    def set_color(self, arg_new_color):
        """ set_color """
        if arg_new_color < self.MIN_COLOR_INDEX or arg_new_color > self.MAX_COLOR_INDEX:
            Msg.warning("syntax error, invalid cell color")
            return
        self.color = arg_new_color

    def reset_color(self):
        """ reset_color """
        self.color = self.DEFAULT_COLOR

    def random_color(self):
        """ random_color """
        self.color = random.randint(self.MIN_COLOR_INDEX, self.MAX_COLOR_INDEX)

    def random_cell(self):
        """ random_cell """
        self.color = random.randint(self.OBSTACLE_COLOR, self.MAX_COLOR_INDEX)

    def recalculate_color(self, arg_algorithm_index=1):
        """ recalculate_color """

        color = self.get_color()

        if arg_algorithm_index == 1:
            color = (((4 * color) + 23) % (self.MAX_COLOR_INDEX + 1))

        self.set_color(color)

    def get_representation(self):
        """ get_representation """

        if self.get_occupying_ant() is None:
            return_string = str(self.get_color())
        else:
            return_string = Color.red(self.get_occupying_ant().get_name())

        return_string = Sty.bold(return_string)

        if self.get_color() == 0:
            return_string = Bg.white(Color.white(return_string))
        elif self.get_color() == 1:
            return_string = Bg.yellow(Color.yellow(return_string))
        elif self.get_color() == 2:
            return_string = Bg.blue(Color.blue(return_string))
        elif self.get_color() == 3:
            return_string = Bg.green(Color.green(return_string))
        elif self.get_color() == 4:
            return_string = Bg.cyan(Color.cyan(return_string))
        else:
            return_string = Sty.framed(Bg.black(Color.black("*")))

        return return_string
