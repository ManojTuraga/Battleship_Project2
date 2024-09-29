'''
Module: board_util.py
Creation Date: September 11th, 2024
Author: Team 19 Devs
Contributors: Manoj Turaga
Sources:

Description:
    This is the "remnants" of the original battleship program. Due to the nature
    of the inital program, we place all board related utlity functions in this
    file. We wanted to reserve logic to the code in main.py

Inputs:
    None
Outputs:
    None

Sources: GeeksforGeeks/Team 42 initial Battleship implementation
'''
###############################################################################
# Imports
###############################################################################
import ai
import events

###############################################################################
# Variables
###############################################################################

# Define a variable to store the size of the board
boardSize = 10

# Define the letters that represents the name
# of the columns
letters = "ABCDEFGHIJ"

# Create a dictionary that will store the size of the
# ship based on its ID. This will be used to determine
# the amount of lives that a particular ship has
shipSizes = {
    1: [1],
    2: [1, 2],
    3: [1, 2, 3],
    4: [1, 2, 3, 4],
    5: [1, 2, 3, 4, 5]
}

###############################################################################
# Procedure 
###############################################################################
def printBoard(board):
    """
    Function: Print Board

    Description: This function displays a visaul representation of a board
                 the system representation of the board

    Inputs: System Board
    Outputs: Prints board to console
    """
    # Initially go through and print the column labls
    print("   " + "  ".join(letters))

    # For every possible row in the board convert every call
    # into a string representation of itself and print the cell
    # to the console
    for i in range(boardSize):
        row = [str(cell) for cell in board[i]]

        # The reason for all these replaces is to make the game
        # display the board more cleanly. We know this is goofy
        # but we thought it would be fun to preserve aS much of
        # the original logic of the game as possible
        print((f"{i + 1:2} {' '.join(row)}").replace("~", "Q").replace("Q", "~~").replace("O", "Q").replace("Q", "OO").replace("X", "Q").replace("Q", "XX"))

def createEmptyBoard():
    """
    Function: Create Empty Board

    Description: This function returns a instance of a battleship
                 board with the board in the empty state 

    Inputs: None
    Outputs: NxN default instance of battleship board
    """

    # In this implementation, we say that the board is
    # empty when all the cells in the board are '~'
    return [['~'] * boardSize for _ in range(boardSize)]

def getCoordinatesInput(): #gets coordinates
    """
    Function: Get Coordinate Input

    Description: This function is the method that allows the user to input coordinates
                 of interest, whether that be when placing ships or triggering an
                 attack
    
    Inputs: User Input
    Outputs: System represenation of inputted coordinate
    """
    # We only return from the function when the input is deemed
    # to be valid
    while True:
        # Obtain the row and column from the user in the form
        # ColRow and remove any format characters while standardizing
        # the input
        coordinates = input("Enter the coordinates (e.g. A5): ").strip().upper()

        # The input needs to be at least 2 characters long.
        # We can then have this condition as an optimization
        # in trying to determine if the input is valid
        if len(coordinates) < 2:
            print("Invalid input. Try again.")
            continue
        
        # We can assume that column names will only be one character
        # and it will typically be first character, so assume any
        # trailing characters are the row identifier
        col, row = coordinates[0], coordinates[1:]

        # If both the row and the column are valid, then we can
        # convert the strings into their numeric repreesentations
        # and return back to the user
        if col in letters and row.isdigit() and 1 <= int(row) <= 10:
            return letters.index(col), int(row) - 1
        
        # If we were not able to parse a valid coordinate from the input,
        # Indicate that the input is valid and have the loop try again.
        print("Invalid coordinates. Try again.") #if invalid, ask again

def placeShipOnBoard(board, size, shipId, ai_player=False): #places a ship on the board
    """
    Function: Place Ships on Board

    Description: This function is responsible for placing ships on the board, for both
                 AI and not AI players. This is technically not a "utility" function
                 as the way this is implemented has been changed to accomodate a larger
                 feature set but we decided to keep it in this module due to its use in
                 the original implementation

    Inputs: Player Board, Size of the Ship, Ship ID, if the player is an AI
    Outputs: Modified player board with ship placements
    """
    # It could be the case that the AI picks a coordinate that
    # is invalid. The human does not have to worry about this in
    # this function because the get coordinates function has the
    # placement checking
    while True:
        # If the current player is an AI, rely on the AI module to
        # to get the coordinates of the ship placement. Otherwise,
        # get it from user input
        if ai_player:
            row, col, orientation = ai.generateAICoords(is_setup=True)
        else:
            col, row = getCoordinatesInput() #get coordinates
            orientation = input("Enter H (Horizontal) or V (Vertical): ").strip().upper()#get orientation
        
        # The following three variables are created to help combine common code
        # The only thing that is different from this point onwards is if we place
        # the ship horizontally or vertically, so we will define a comparison base
        # and a set of increment functions to handle the horizontal and vertical case
        base = None
        row_func = None
        col_func = None
        
        if orientation == "H":
            base = col
            row_func = lambda inc: row
            col_func = lambda inc : col + inc

        elif orientation == "V":
            base = row
            row_func = lambda inc: row + inc
            col_func = lambda inc : col

        else:
            # The AI is expected to hit this point since the ship generation
            # is random but if a player reaches here, then they picked an invalid
            # coordinate
            if not ai_player: print("Invalid orientation. Try again.") #if orientation is invalid
            continue
        
        # If the result of placing the ships means not every coordinate is within
        # the range of the board or if there are intersecting placements, do not
        # accept this start coordinate and instead make the player pick again
        if base + size > boardSize or any(board[row_func( i )][col_func( i )] != '~' for i in range(size)):
            if not ai_player: 
                print("Invalid placement. Try again.")
                continue

        else:
            # Place the ship on the board. At the same time, put these placements
            # on the AI as well since the 3rd level AI knows exactly where the
            # ship are
            for i in range(size): #loop through board
                if not ai_player:  ai.OPPONENT_LOCATION.append((row_func( i ), col_func( i )))
                board[row_func( i )][col_func( i )] = shipId #place ship
            
            # Show the current player the fruits of their labor
            if not ai_player:
                print("\nCurrent board:")
                printBoard(board)
            break

def placeShips(board, shipSizes, ai_player=False):
    """
    Function: Place Ships

    Description: This is a function that allows the calling entity to place
                 n number of ships at once.

    Inputs: Player Board, Sizes of Ships, if the player is an AI
    Outputs: Modified player board with ship placements
    """
    # For every ship size that is to be placed
    # place that ship on the board and show the fruits of labor
    # to the user
    for i, size in enumerate(shipSizes):
        print("\nCurrent board:")
        printBoard(board)
        placeShipOnBoard(board, size, f"S{i+1}", ai_player)
        events.clear_terminal()

def allShipsSunk(shipHits):
    """
    Function: All Ships Sunk

    Description: This function determines if every ship that was
                 place is now sunk.

    Inputs: Dictionary mapping ship ids to health
    Outputs: Boolean indicated if all ships have a health of 0
    """
    # all will return true only if all ships in the ship
    # hits dictionary are 0
    return all(hit == 0 for hit in shipHits.values())
