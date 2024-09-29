'''
Module: ai.py
Creation Date: September 23rd, 2024
Author: Connor Forristal
Contributors: Connor Forristal, Manoj Turaga

Description:
    This module is our implemenation for the Battleship AI. This module will act
    as a player that will provide coordinates in the place of a human. Three levels
    of AI are supported, where level one gives coordinates at random, level two
    attacks at random until a coordinate is found, and level three knows all of
    the opponents placements

Inputs:
    The placements of your ships
Outputs:
    Coordinates of interest

Sources:
'''
###############################################################################
# Imports
###############################################################################
import random
import board_util

###############################################################################
# Variables
###############################################################################
# All AIs use this as a way to know if a particular coordinate was
# already attacked
USED_COORDS = set()

# The medium AI will maintain a stack of coordinates to visit
# in the event it found a coordinate that was a hit
STACK = []
SHIP_HIT = False 

# The hard AI will maintain a list of all the ship placements
# so you can't hide from its all seeing eye
OPPONENT_LOCATION = []
    
def generateAICoords(is_setup=False):
    """
    Function: Generate AI Coordinates

    Description: This function can be used to generate randome coodinates.
                 It can be used as a set up tool or in attacks. For targetted
                 AI coordinates, the calling entitiy should pop from the
                 stack correspoinding to the AI level

    Inputs: If this is the setup phase of the game
    Outputs: Random coordinate and optionally a direction
    """
    # We need this in a loop to make sure that we get a unique
    # random coordinate in all cases
    while True:
        # Get a random row and column
        row = random.choice([i for i in range(board_util.boardSize)])
        col = random.choice([j for j in range(board_util.boardSize)])
        
        # If we are in the setup phase, also add a random direction
        if is_setup:
            direction = random.choice(["H", "V"])
            return (row, col, direction)

        # If we are not in the setup phase annd the random coordinate
        # is unique, return the coordinate back to the calling function
        if (row, col) not in USED_COORDS:
            USED_COORDS.add((row, col))
            return (row, col)

def stack_directions(row, col):
    """
    Function: Stack Directions 

    Description: This code is used for the level 2 AI, which determines
                 the next possible coordinates to attack given the current
                 coordinate was successful hit.

    Inputs: Row and Column
    Outputs: nothing
    """
    # It is possible that the 4 orthogonal coordinates to the current
    # coordinate either don't exist or have already been used, so make sure
    # to only use directions that make sense to access
    possible_directions = choose_direction(row, col)
    
    # Create a list that contains a set of coordinates that the AI
    # should target next
    for i in range(len(possible_directions)):
        possible_directions[i] = next_location(possible_directions[i], row, col)
        
    # Add these new coordinates to the stack
    STACK.extend(possible_directions)

def determine_ai_player():
    """
    Function: Determine AI Player 

    Description: This code is part of the entire game setup operation where the
                 the player is able to determine if they want to play against an
                 AI

    Inputs: User Input
    Outputs: If the opponent is an AI and it's difficulty
    """
    # Initalize the ai player and the difficulty
    # to indicate that the opponent is a human
    ai_player, difficulty = False, None 
    
    # Keep accepting inputs until the selections are all
    # valid
    while True:
        ai_player = input("Do you want to play against an AI? (Y/N): ").strip()

        # If the player wants to play against an AI, obtain
        # difficulty of the ai as another prompt
        if ai_player in ["Y", "y", "yes"]:
            ai_player = True
            
            diff_hash = {"1" : 1, "Easy" : 1, "easy" : 1, 
                         "2" : 2, "Medium" : 2, "medium" : 2, 
                         "3" : 3, "Hard" : 3, "hard" : 3}
            
            # Keep trying to get a valid input from the user
            while True:
                difficulty = input("Select Ai difficulty:\n1) Easy\n2) Medium\n3) Hard\n-> ").strip()
                if difficulty in diff_hash.keys():
                    difficulty = diff_hash[difficulty]
                    break
                print("Invalid input.")
            
            break
        
        # If the player doesn't want to play against an AI,
        # INdicate that the other player will not be an AI
        elif ai_player in ["N", "n", "no"]:
            ai_player = False 
            break
        
        print("Invalid input.")
    
    return (ai_player, difficulty)


def next_location(direction, row, col):
    """
    Function: Next Location

    Description: This function is a helper function that returns the next possible
                 coordinate given a direction. Note that this function does not have
                 any runtime checks and instead relies on the checks done by the
                 calling function

    Inputs: Direction of next coordinate, current coordinate
    Outputs: Location of next coordinate
    """
    # Essentially, given the current coordinate, compute the location of the
    # next coordiante using the direction. The direction uses the same
    # nomenclature as the main cardinal directions on a compass, so direction
    # of computation is normalized given that north is always pointing upwards
    if direction == "W":
        return (row, col - 1)
    elif direction == "S":
        return (row + 1, col)
    elif direction == "E":
        return (row, col + 1)
    elif direction == "N":
        return (row - 1, col)


def choose_direction(row, col):
    """
    Function: Choose Coordiantes

    Description: This function is a helper function that determines all the possible
                 orthogonal coordiantes that can be visited from the current coordinate,
                 given that the orthogonal coordinate has not already been visited before

    Inputs: Current coordinate
    Outputs: Directions of next coordinate.
    """
    # Initally, all 4 cardinal directions are possible spots for the next
    # coodinate, so initialize a list containing all four possible
    # directions
    possible_directions = ["N", "E", "S", "W"]
    
    # Much like the next_location function, we look at all the coordinates
    # that exist and if that coordinate is not valid or has already been
    # visited, remove it
    if row + 1 >= board_util.boardSize or (row + 1, col) in USED_COORDS:
        possible_directions.remove("S")
    
    if col + 1 >= board_util.boardSize or (row, col + 1) in USED_COORDS:
        possible_directions.remove("E")
        
    if row - 1 < 0 or (row - 1, col) in USED_COORDS:
        possible_directions.remove("N")
    
    if col - 1 < 0 or (row, col - 1) in USED_COORDS:
        possible_directions.remove("W")

    # Return the possible directions as list back to the calling function
    return possible_directions
        
    
    