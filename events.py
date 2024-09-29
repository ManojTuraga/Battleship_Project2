'''
Module: events.py
Creation Date: September 28nd, 2024
Author: Manoj Turaga
Contributors: Manoj Turaga

Description:
    This module is the "events" module where common events that occur can simply
    be called using this module. We have events like trigger input from the user,
    displaying a message, or just clearing the console.

Inputs:
    User Input (Optionally)
Outputs:
    Modifications to the console

Sources: GeeksforGeeks/Team 42 initial Battleship implementation
'''
###############################################################################
# Imports
###############################################################################
import platform
import os

###############################################################################
# User Input Events
###############################################################################
def trigger_player_selection( init_msg, options, selection_msg, display_invalid, should_clear_terminal ):
    """
    Function: Trigger Player selection

    Description: This is an event that can be triggered by the calling function
                 if they want input from the user.

    Inputs: Initial Message, List of options, Prompt message, whether the invalid
            input text should be displayed, should the console be cleared\
            
    Outputs: Prompt for user input
    """
    # If the calling function wants to clear the terminal, then the
    # terminal is cleared
    if should_clear_terminal:
        clear_terminal()

    # The init_msg paramter can have None passed in if the calling function
    # chooses to not have this funtion
    if init_msg is not None:
        print( init_msg )

    # For every option in the list of options, print the option
    # back to the user along with the corresponding selection id
    for i, option in enumerate( options, 1 ):
        print( f"{ i }. { option }" )

    print()

    # Display the invalid input message if the error checks find that the
    # previous input is invalid
    if display_invalid:
        print( "Error! Invalid Selection" )

    # Get the input from the user
    choice = input( selection_msg )

    # If the type of the return is a string type, remove any of the
    # formatting
    if type( choice ) == str:
        choice = choice.strip()

    return choice

###############################################################################
# Display Events
###############################################################################
def clear_terminal():
    """
    Function: Clear Terminal

    Description: This is an event that can be triggered if the dev wants to clear
                 the terminal. This is inspired by what the devs of Team 42 did.

    Inputs: None
    Outputs: Clears the console

    Sources: GeeksforGeeks/Team 42 Implementation
    """
    # Since we want this program to be platform independent, we would like to
    # call the custom clear screen method for the system's terminal
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def display_messages( msgs, should_clear_terminal ):
    """
    Function: Display Messages

    Description: This is an event that can be triggered if the dev wants to display
                 a list of messages to the console

    Inputs: List of message, if the terminal should be cleared beforehand
    Outputs: Displays Messages on console
    """
    # If the clear terminal flag was set, call the function
    # to clear the terminal
    if should_clear_terminal:
        clear_terminal()

    # For ever message in the list of messages, print the message to the console
    for msg in msgs:
        print( msg )

