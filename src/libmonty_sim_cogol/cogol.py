#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from dataclasses import dataclass, field
import numpy as np


@dataclass
class Grid:
    height: int
    width: int
    is_loopback: bool
    _alive_set: set[tuple[int, int]] = field(default_factory=set)

    def add_glider(self, x: int, y: int, rotations: int = 0) -> None:
        glider = np.array([[0, 1, 0],
                           [0, 0, 1],
                           [1, 1, 1]],
                          int)

        glider = np.rot90(glider, rotations)

        glider_alive_cells = set()

        for row in range(3):
            for col in range(3):
                if glider[row][col] == 1:
                    glider_alive_cells.add((x + row, y + col))

        self._alive_set = self._alive_set.union(glider_alive_cells)

    def advance(self):
        new_set = set()
        for row in range(self.height):
            for col in range(self.width):
                alive_neighbors = self._alive_set.intersection(self._get_cell_neighbors(row, col))

                # Any live cell with fewer than two live neighbours dies, as if by underpopulation.
                # Any live cell with two or three live neighbours lives on to the next generation.
                # Any live cell with more than three live neighbours dies, as if by overpopulation.
                # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

                if self.is_cell_alive(row, col) and len(alive_neighbors) in {2, 3}:
                    new_set.add((row, col))
                elif not self.is_cell_alive(row, col) and len(alive_neighbors) == 3:
                    new_set.add((row, col))

        self._alive_set = new_set

    def is_cell_alive(self, row: int, col: int):
        return True if (row, col) in self._alive_set else False

    def _get_cell_neighbors(self, row: int, col: int) -> set[tuple[int, int]]:
        neighbors = set()

        for rel_row in range(row - 1, row + 2):
            if rel_row == -1:
                if self.is_loopback:
                    rel_row = self.height - 1
                else:
                    continue
            elif rel_row == self.height:
                if self.is_loopback:
                    rel_row = 0
                else:
                    continue
            else:
                pass

            for rel_col in range(col - 1, col + 2):

                if rel_row == row and rel_col == col:
                    continue

                if rel_col == -1:
                    if self.is_loopback:
                        rel_col = self.width - 1
                    else:
                        continue
                elif rel_col == self.width:
                    if self.is_loopback:
                        rel_col = 0
                    else:
                        continue
                else:
                    pass

                neighbors.add((rel_row, rel_col))

        return neighbors

    @property
    def is_empty(self) -> bool:
        return True if self._alive_set == set() else False


def print_grid(grid: Grid) -> None:
    print('-' * grid.width * 2)
    for row in range(grid.height):
        for col in range(grid.width):
            cell_display = ' X' if grid.is_cell_alive(row, col) else ' _'
            print(f'{cell_display:>2}', end='')
        print('')
    print('-' * grid.width * 2)


def grid_to_color_bytes(grid: Grid) -> bytes:
    color_bytes = b''
    for row in range(grid.height):
        for col in range(grid.width):
            color_bytes += b'\xFF\xFF\xFF' if grid.is_cell_alive(row, col) else b'\x00\x00\x00'
    return color_bytes
