'''
Module: utility.py
Date Created: September 17, 2024
Author: Manoj Turaga
Contributer(s): Manoj Turaga

Description: This module is a utility module common code and helper
             functions

Sources: Team 42 Battleship project
'''

# Import system and name from the OS module. We will
# need to be able to clear the screen when executing
# a new command, and this will allow us to start with
# a clean screen
#
# Source: Team 42 Battleship Project
from os import system, name

################################################################################
# Global Variables and Constants
################################################################################
WINDOWS_OS_NAME : str = "nt"
WINDOWS_OS_CLEAR_SCREEN_COMMAND : str = "cls"

NON_WINDOWS_OS_CLEAR_SCREEN_COMMAND : str = "clear"

def clear_screen():
        """
        Function: Clear Screen

        Inputs: None
        Outputs: Removes characters in standard output window

        Description: This is a helper function that will clear the screen
                     when called. Used to make clean output
        
        Sources: Team 42 Battleship Project
        """
        if name == WINDOWS_OS_NAME:
            # Execute the windows version of the clear screen command
            system( WINDOWS_OS_CLEAR_SCREEN_COMMAND )

        else:
            # Execute the non windows version of the clear screen command
            system( NON_WINDOWS_OS_CLEAR_SCREEN_COMMAND )