#!/usr/bin/env python3

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

""" grid """

# imports: project
from quadrille_lants.components.cell import Cell
from quadrille_lants.components.ant import Ant
from quadrille_lants.utils.regex import Regex


class Grid:
    """ Grid """

    def __init__(self):
        self._ls_rows = list()
        self._i_height = 0
        self._i_width = None  # invalid initial value for checking #
        self._ls_ants = list()

    def delete_all_rows(self):
        self._ls_rows = list()

    def _refresh_height(self):
        self._i_height = len(self._ls_rows)

    def load_row(self, s_row):
        i_row = self._i_height

        if self._i_width is None:
            self._i_width = len(s_row)

        if len(s_row) != self._i_width:
            raise ValueError("bad row length: {} != {}".format(len(s_row), self._i_width))

        ls_cols = list()

        for i_char, s_char in enumerate(s_row):
            i_col = i_char

            parsed = Regex.parse_ant_any(s_char)

            if parsed is not None:
                o_cell = Cell(0)  # initial color for cell with ant set to 0 (no requirements) #
                new_ant = Ant(parsed["name"], i_row, i_col)
                if new_ant in self._ls_ants:
                    raise ValueError("semantic error, ant already exists")
                self._ls_ants.append(new_ant)
                self._ls_ants.sort()
                o_cell.set_occupying_ant(new_ant)
                ls_cols.append(o_cell)
                continue

            parsed = Regex.parse_color_any(s_char)

            if parsed is not None:
                ls_cols.append(Cell(int(parsed["color"])))
                continue

            parsed = Regex.parse_obstacle(s_char)

            if parsed is not None:
                ls_cols.append(Cell(-1))
                continue

            raise ValueError("syntax error, illegal character in the game file")

        self._ls_rows.append(ls_cols)

        self._refresh_height()

    def get_ant_count(self):
        return len(self._ls_ants)

    def get_ants(self):
        return self._ls_ants

    def get_ant(self, s_ant_name):
        """ get_ant """

        s_ant_name = s_ant_name.lower()

        for o_ant in self._ls_ants:
            if o_ant.get_name() == s_ant_name:
                return o_ant

        # if an ant was not found, None is returned #
        return None

    def add_ant(self, s_name, i_pos_row, i_pos_column):

        if self.get_ant(s_name) is not None:
            raise ValueError("an ant with this name already exists")

        if i_pos_row > self._i_height or i_pos_column > self._i_width:
            raise ValueError("no cell exists at the indices given")

        if self._ls_rows[i_pos_row][i_pos_column].get_occupying_ant() is not None:
            raise ValueError("the cell at the given indices is already occupied by another ant")

        if self._ls_rows[i_pos_row][i_pos_column].is_obstacle():
            raise ValueError("the cell at the given indices contains an obstacle")

        o_ant = Ant(s_name, i_pos_row, i_pos_column)
        self._ls_ants.append(o_ant)
        self._ls_ants.sort()
        self._ls_rows[i_pos_row][i_pos_column].set_occupying_ant(o_ant)

    def remove_ant(self, o_ant):
        self._ls_ants.remove(o_ant)
        self.cell_remove_ant(o_ant.get_pos_row(), o_ant.get_pos_column())

    def get_height(self):
        return self._i_height

    def get_width(self):
        return self._i_width

    def get_cell(self, i_row, i_col):
        return self._ls_rows[i_row][i_col]

    def recalculate_cell_color(self, i_row, i_col):
        self._ls_rows[i_row][i_col].recalculate_color()

    def cell_remove_ant(self, i_row, i_col):
        self._ls_rows[i_row][i_col].remove_occupying_ant()

    def cell_set_ant(self, i_row, i_col, o_ant):
        self._ls_rows[i_row][i_col].set_occupying_ant(o_ant)

    def cell_reset_color(self, i_row, i_col):
        self._ls_rows[i_row][i_col].reset_color()

    def cell_randomize(self, i_row, i_col):
        self._ls_rows[i_row][i_col].random_cell()

    def cell_make_obstacle(self, i_row, i_col):
        self._ls_rows[i_row][i_col].make_obstacle()

    def cell_random_color(self, i_row, i_col):
        self._ls_rows[i_row][i_col].random_color()
