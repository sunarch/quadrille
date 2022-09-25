#!/usr/bin/env python3
# -*- coding: utf-8, vim: expandtab:ts=4 -*-

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# imports: library
import sys

# imports: project
from quadrille_lants.components.grid import Grid
from quadrille_lants.utils.outputmessages import OutputMessages as Msg
from quadrille_lants.utils.regex import Regex

################################################################################
#  Langton Ants ################################################################
################################################################################
#  An extended version of the original Langton Ants simulation #################
################################################################################

# global variables #############################################################

rule = [270, 90, 315, 45, 90]
speedup = 2
round_count = 0


# control function definitions #################################################

# perform_ant_actions ##########################################################

def perform_ant_actions(o_grid, arg_ant):
    """ perform_ant_actions """

    if arg_ant is None:
        return o_grid

    ant_origin_pos_row = arg_ant.get_pos_row()
    ant_origin_pos_column = arg_ant.get_pos_column()
    ant_origin_cell = o_grid.get_cell(ant_origin_pos_row, ant_origin_pos_column)

    ant_target_pos_row, ant_target_pos_column = arg_ant.calc_target_row_n_col()

    try:
        ant_target_cell = o_grid.get_cell(ant_target_pos_row, ant_target_pos_column)
    except IndexError as err:
        Msg.error(str(err))
        o_grid = ui_function_escape(o_grid, list(arg_ant.get_name()))
        return o_grid

    # move if possible #
    if ant_target_cell.has_occupying_ant() or ant_target_cell.is_obstacle():
        ant_target_cell = ant_origin_cell
        ant_target_pos_row = ant_origin_pos_row
        ant_target_pos_column = ant_origin_pos_column
    else:
        arg_ant.set_position(ant_target_pos_row, ant_target_pos_column)

        o_grid.cell_remove_ant(ant_origin_pos_row, ant_origin_pos_column)
        o_grid.cell_set_ant(ant_target_pos_row, ant_target_pos_column, arg_ant)

    # turn
    ant_target_cell_original_color = ant_target_cell.get_color()
    arg_ant.change_orientation(rule[ant_target_cell_original_color])

    # change cell color based on formula #
    o_grid.recalculate_cell_color(ant_target_pos_row, ant_target_pos_column)

    # if everything went in order #
    return o_grid


# decorator: print_grid_after ##################################################

def print_grid_after(arg_function):
    """ print_grid_after """

    def new_function(o_grid, arguments):
        """ new_function """

        arg_function(o_grid, arguments)
        o_grid = ui_function_print(o_grid, list())

        return o_grid

    return new_function


# decorator: print_result ######################################################

def print_result(arg_function):
    """ print_result """

    def new_function(o_grid, arguments):
        """ new_function """

        result = arg_function(o_grid, arguments)

        if result is not None:
            print(str(result))

        return o_grid

    return new_function


# user interface definitions ###################################################

# ui_function_quit #############################################################

def ui_function_quit(o_grid, arguments):
    """ ui_function_quit """

    if len(arguments) > 0:
        Msg.warning("too many parameters")
        return o_grid

    sys.exit(0)
# BREAKPOINT #


# ui_function_print ############################################################

# reference function for @printGridAfter
def ui_function_print(o_grid, arguments):
    """ ui_function_print """

    if len(arguments) > 0:
        Msg.warning("too many parameters")
        return o_grid

    for i_row in range(0, o_grid.get_height()):
        row_string = ""

        for i_col in range(0, o_grid.get_width()):
            cell = o_grid.get_cell(i_row, i_col).get_representation()

            row_string += cell

        print(row_string)

    return o_grid


# ui_function_ant ##############################################################

def ui_function_ant(o_grid, arguments):
    """ ui_function_ant """

    if len(arguments) > 0:
        Msg.warning("too many parameters")
        return o_grid

    s_result = ""

    for o_ant in o_grid.get_ants():
        if s_result != "":
            s_result += ", "

        s_result += o_ant.get_name()

    print("The following ants are on the grid: " + s_result)

    return o_grid


# ui_function_reset ############################################################

@print_grid_after
def ui_function_reset(o_grid, arguments):
    """ ui_function_reset """

    if len(arguments) > 0:
        Msg.warning("too many parameters")
        return o_grid

    for i_row in range(0, o_grid.get_height()):
        for i_col in range(0, o_grid.get_width()):
            o_grid.cell_reset_color(i_row, i_col)

    Msg.info("the grid cells have been reset")

    return o_grid


# ui_function_random ###########################################################

@print_grid_after
def ui_function_random(o_grid, arguments):
    """ ui_function_random """

    if len(arguments) > 0:
        Msg.warning("too many parameters")
        return o_grid

    for i_row in range(0, o_grid.get_height()):
        for i_col in range(0, o_grid.get_width()):
            o_grid.cell_randomize(i_row, i_col)

    Msg.info("the grid cells have been randomized")

    return o_grid


# ui_function_arcade ###########################################################

@print_grid_after
def ui_function_arcade(o_grid, arguments):
    """ ui_function_arcade """

    if len(arguments) > 0:
        Msg.warning("too many parameters")
        return o_grid

    for i_row in range(0, o_grid.get_height()):
        for i_col in range(0, o_grid.get_width()):
            if i_row == 0 or i_row == (o_grid.get_height() - 1) or i_col == 0 or i_col == (o_grid.get_width() - 1):
                o_grid.cell_make_obstacle(i_row, i_col)
            else:
                o_grid.cell_random_color(i_row, i_col)

    for ant in o_grid.get_ants():
        row = ant.get_pos_row()
        column = ant.get_pos_column()

        if row == 0 or row == (o_grid.get_height() - 1) or column == 0 or column == (o_grid.get_width() - 1):
            ui_function_escape(o_grid, list(ant.get_name()))

    Msg.info("a random arcade grid has been created")

    return o_grid


# ui_function_step #############################################################

def ui_function_step(o_grid, arguments):
    """ ui_function_step """

    if len(arguments) > 0:
        Msg.warning("too many parameters")
        return o_grid

    o_grid = ui_function_move(o_grid, list("1"))
    Msg.info("one move has been made")

    return o_grid


# ui_function_move #############################################################

@print_grid_after
def ui_function_move(o_grid, arguments):
    """ ui_function_move """

    global round_count

    if len(arguments) < 1:
        Msg.warning("missing parameter")
        return o_grid

    if len(arguments) > 1:
        Msg.warning("too many parameters")
        return o_grid

    # arguments[0] is move count
    parsed = Regex.parse_count(arguments[0])

    if parsed is None:
        Msg.warning("invalid argument")
        return o_grid

    count = int(parsed["count"])

    if count == 0:
        # if 0 is given, no moves are made #
        return o_grid

    for i_new_round in range(1, count + 1):
        round_count += 1

        for o_ant in o_grid.get_ants():
            current_ant_type = o_ant.get_type()

            if current_ant_type == "standard":
                o_grid = perform_ant_actions(o_grid, o_ant)
                continue

            if current_ant_type == "busy":
                for i in range(1, speedup + 1):
                    o_grid = perform_ant_actions(o_grid, o_ant)
                continue

            if current_ant_type == "lazy":
                if ((round_count - 1) % speedup) == 0:
                    o_grid = perform_ant_actions(o_grid, o_ant)
                continue

    return o_grid


# ui_function_position #########################################################

def ui_function_position(o_grid, arguments):
    """ ui_function_position """

    if len(arguments) < 1:
        Msg.warning("missing parameter")
        return o_grid

    if len(arguments) > 1:
        Msg.warning("too many parameters")
        return o_grid

    ant_name = arguments[0]

    ant = o_grid.get_ant(ant_name)

    if ant is None:
        Msg.warning("invalid parameter, no ant with the given name: '{}'".format(ant_name))
        return o_grid

    print("The position of ant '" + ant_name + "' is: " + ant.get_position_str())

    return o_grid


# ui_function_field ############################################################

def ui_function_field(o_grid, arguments):
    """ ui_function_field """

    if len(arguments) < 1:
        Msg.warning("missing parameter")
        return o_grid

    if len(arguments) > 1:
        Msg.warning("too many parameters")
        return o_grid

    arg_coordinates = arguments[0]

    parsed = Regex.parse_coordinates(arg_coordinates)

    if parsed is None:
        Msg.warning("syntax error in the parameter")
        return o_grid

    row = int(parsed["row"])
    column = int(parsed["column"])

    # values < 0 have been eliminated at parsing
    if row > o_grid.get_height() or column > o_grid.get_width():
        Msg.warning("no cell exists at the indices given")
        return o_grid

    s_msg = "The field in the {}. row and the {}. column has the color: {}"
    print(s_msg.format(str(row + 1), str(column + 1), o_grid.get_cell(row, column).get_representation()))

    return o_grid


# ui_function_direction ########################################################

def ui_function_direction(o_grid, arguments):
    """ ui_function_direction """

    if len(arguments) < 1:
        Msg.warning("missing parameter")
        return o_grid

    if len(arguments) > 1:
        Msg.warning("too many parameters")
        return o_grid

    ant_name = arguments[0]

    ant = o_grid.get_ant(ant_name)

    if ant is None:
        Msg.warning("invalid parameter, no ant with the given name: '{}'".format(ant_name))
        return o_grid

    print(ant.get_orientation_str())

    return o_grid


# ui_function_create ###########################################################

def ui_function_create(o_grid, arguments):
    """ ui_function_create """

    if len(arguments) < 1:
        Msg.warning("missing parameter")
        return o_grid

    if len(arguments) > 1:
        Msg.warning("too many parameters")
        return o_grid

    parsed = Regex.parse_ant_data(arguments[0])

    if parsed is not None:
        new_ant_name = parsed["name"]
        new_ant_pos_row = int(parsed["row"])
        new_ant_pos_column = int(parsed["column"])
    else:
        Msg.warning("syntax error in the parameter")
        return o_grid

    try:
        o_grid.add_ant(new_ant_name, new_ant_pos_row, new_ant_pos_column)
    except ValueError as e:
        Msg.warning(str(e))
        return o_grid

    s_msg = "Created a new ant '{}' in the {}. row and the {}. column."
    Msg.info(s_msg.format(new_ant_name, new_ant_pos_row, new_ant_pos_column))


# ui_function_escape ###########################################################

def ui_function_escape(o_grid, arguments):
    """ ui_function_escape """

    if len(arguments) < 1:
        Msg.warning("missing parameter")
        return o_grid

    if len(arguments) > 1:
        Msg.warning("too many parameters")
        return o_grid

    ant_name = arguments[0]

    parsed = Regex.parse_ant_any(ant_name)

    if parsed is None:
        Msg.warning("invalid ant name")
        return o_grid

    ant = o_grid.get_ant(ant_name)

    if ant is None:
        Msg.warning("invalid parameter, no ant with the given name: '{}'".format(ant_name))
        return o_grid

    o_grid.remove_ant(ant)

    Msg.info("Ant '" + ant_name + "' has been deleted.")

    if o_grid.get_ant_count() < 1:
        Msg.warning("all ants have left the game grid")

    return o_grid


# ui_function_help #############################################################

def ui_function_help(o_grid, arguments):
    """ ui_function_help """

    global ui_functions_dict
    global ui_command_list

    if len(arguments) > 0:
        Msg.warning("too many parameters")
        return o_grid

    for command in ui_command_list:
        print(str(command))

    return o_grid


# user interface command dictionary ############################################

ui_functions_dict = {
    # UI commands with zero (0) arguments #

    "quit":    ui_function_quit,
    "exit":    ui_function_quit,
    "q:":      ui_function_quit,
    "print":   ui_function_print,
    "ant":     ui_function_ant,
    "reset":   ui_function_reset,
    "step":    ui_function_step,
    "s:":      ui_function_step,
    "random":  ui_function_random,
    "arcade":  ui_function_arcade,
    "help":    ui_function_help,

    # UI commands with one (1) arguments #

    "move":       ui_function_move,
    "position":   ui_function_position,
    "pos":        ui_function_position,
    "field":      ui_function_field,
    "direction":  ui_function_direction,
    "create":     ui_function_create,
    "escape":     ui_function_escape,
    "remove":     ui_function_escape,
    "delete":     ui_function_escape,
    "del":        ui_function_escape
}
ui_command_list = list(ui_functions_dict.keys())


# gamefile loader ##############################################################

def load_gamefile(o_grid, s_file_name):

    o_grid.delete_all_rows()

    ls_file_rows = list()

    with open(s_file_name, 'r') as game_file:
        for line in game_file:
            ls_file_rows.append(line.strip())

    if len(ls_file_rows) < 1:
        Msg.error("no lines in game file")
        sys.exit(1)
# BREAKPOINT #

    for s_row in ls_file_rows:
        try:
            o_grid.load_row(s_row)
        except ValueError as e:
            print(str(e))
            sys.exit(1)
# BREAKPOINT #

    return o_grid


# begin main control flow ######################################################

arg_list = sys.argv
filename = arg_list.pop(0)
argument_count = len(arg_list)

if argument_count < 1:
    Msg.error("missing command line argument")
    sys.exit(1)
# BREAKPOINT #

g_o_grid = Grid()

s_game_file_name = arg_list[0]
g_o_grid = load_gamefile(g_o_grid, s_game_file_name)

if argument_count > 1:

    for n in range(1, argument_count):

        parsed = Regex.parse_cla_rule(arg_list[n])
        if parsed is not None:
            new_rule = parsed["value"].split("-")
            for i in range(0, len(rule)):
                rule[i] = int(new_rule[i])
            continue

        parsed = Regex.parse_cla_speedup(arg_list[n])
        if parsed is not None:
            speedup = int(parsed["value"])
            continue

        # else #
        Msg.error("invalid command line argument")
        sys.exit(1)
# BREAKPOINT #

# begin interactive user interface #############################################

while True:
    user_input = input("LangtonAnts $ ")
    input_elements = user_input.split()
    input_element_count = len(input_elements)

    if input_element_count < 1:
        Msg.warning("invalid command")
        continue

    ui_command = input_elements.pop(0)
    # input_elements now only contains the parameters

    if ui_command not in ui_command_list:
        Msg.warning("invalid command")
        continue

    g_o_grid = ui_functions_dict[ui_command](g_o_grid, input_elements)
    continue

# end of main control flow #####################################################
