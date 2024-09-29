###############################################################################
# Imports
###############################################################################
import platform
import os

import scoreboard
import visuals

###############################################################################
# User Input Events
###############################################################################
def trigger_player_selection( init_msg, options, selection_msg, display_invalid, should_clear_terminal ):
    if should_clear_terminal:
        clear_terminal()

    if init_msg is not None:
        print( init_msg )

    for i, option in enumerate( options, 1 ):
        print( f"{ i }. { option }" )

    print()

    if display_invalid:
        print( "Error! Invalid Selection" )

    choice = input( selection_msg )

    if type( choice ) == str:
        choice = choice.strip()

    return choice

###############################################################################
# Display Events
###############################################################################
def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def display_messages( msgs, should_clear_terminal ):
    if should_clear_terminal:
        clear_terminal()

    for msg in msgs:
        print( msg )

