'''
Module: events.py
Creation Date: September 25th, 2024
Author: Clare Channel
Contributors: Clare Channel, Manoj Turaga

Description:
    This module provides the calling entity with metadata about the
    bullet class, including what bullets exist overall, and how each
    bullet affects the bullet.

Inputs:
    The bullet in question (optional)
Outputs:
    Prints information to the console

Sources:
'''

###############################################################################
# Imports
###############################################################################
from bullet import *

###############################################################################
# Types
###############################################################################
# The following is the definition/implementation of the visuals type
class Visuals:
    def __init__(self, board):
        """
        Function: Initialization

        Description: This is the initialization function for the viusals class

        Inputs: the game's board (not used at the moment) 
        Outputs: None
        """
        self.board = board
    
    def display_bullet_types(self):
        """
        Function: Display Bullet Types

        Description: The function gets all the bullets from the
                     bullet module and outputs all the meta information to
                     the console

        Inputs: None
        Outputs: Print Bullet information to the console
        """
        print()
        print("Available Bullets:")

        # Essentially, all the bullets that the game supports is every
        # special bullet plus the standard bullet, so make a temporary
        # list to keep track of that
        all_bullets = [standard_bullet] + all_special_bullet_list

        # For every bullet in the list, print the bullet information
        # to the console
        for bullet in all_bullets:
            print()
            self.display_bullet(bullet)

        #more padding.
        print()

    def display_bullet(self, bullet_in):
        """
        Function: Display Bullet

        Description: The function prints meta information about
                     the bullet in question to the console

        Inputs: Bullet input
        Outputs: Print Bullet information to the console
        """
        # Essentially, the following code prints the following information about
        # the bullet to the console
        #   1. Bullet Name
        #   2. Bullet Description
        #   3. Hit Pattern
        print("-----------------------------")
        print(f"Bullet Name: {bullet_in.name}")
        print(f"Description: {bullet_in.flavor_text}")
        
        # build a string of the displayed bullet hit pattern
        display_string = "Hit Pattern: \n"

        # Get every row from the hit pattern list and independently
        # add it to the output string
        for row in bullet_in.hit_pattern:
            display_string += "  " + " ".join(str(row)) + "\n"

        print(display_string)
        print("-----------------------------")

    def display_hit_pattern_info(self):
        """
        Function: Display Hit pattern Info

        Description: This function displays meta informaation about the hit
                     patterns and what each symbol means

        Inputs: None
        Outputs: Print hit pattern information to the console
        """
        # Hit patterns can contain the following letters
        #   X : The particular cell is being hit
        #   O : The particular cell is revealed
        #   ~ : The particular cell is not acted on
        #   A : There is a chance that this cell is attacked
        #   B : There is a chance that this cell is attacked
        # Display this info to the user
        print("Hit pattern key:")
        print("The center of the pattern is where you aimed at.")
        print("~ means nothing is done to that cell.")
        print("X means that cell is attacked.")
        print("O means that cell is revealed.")
        print("A random 'A' cell in each pattern is attacked.")
        print("A random 'B' cell in each pattern is attacked.")
