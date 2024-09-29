import os
import platform
import ai
import events

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
        # display the board more cleanly
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

def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def getCoordinatesInput(): #gets coordinates
    while True: #loop
        coordinates = input("Enter the coordinates (e.g. A5): ").strip().upper() #get input and format it
        if len(coordinates) < 2: #check if too short
            print("Invalid input. Try again.") #print error message
            continue #continue asking
        col, row = coordinates[0], coordinates[1:] #split input into column and row
        if col in letters and row.isdigit() and 1 <= int(row) <= 10: #check if column and row are valid
            return letters.index(col), int(row) - 1 #return indices
        print("Invalid coordinates. Try again.") #if invalid, ask again

def placeShipOnBoard(board, size, shipId, ai_player=False): #places a ship on the board
        
    while True: #loop
        if ai_player:
            col, row, orientation = ai.generateAICoords(is_setup=True)
        else:
            col, row = getCoordinatesInput() #get coordinates
            orientation = input("Enter H (Horizontal) or V (Vertical): ").strip().upper()#get orientation
        
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
            if not ai_player: print("Invalid orientation. Try again.") #if orientation is invalid
            continue

        if base + size > boardSize or any(board[row_func( i )][col_func( i )] != '~' for i in range(size)): #check fit and availability
            if not ai_player: 
                print("Invalid placement. Try again.") #invalid placement message
                continue #continue asking

        else:
            for i in range(size): #loop through board
                if not ai_player:  ai.OPPONENT_LOCATION.append((row_func( i ), col_func( i )))
                board[row_func( i )][col_func( i )] = shipId #place ship
                
            print("\nCurrent board:")# show board
            printBoard(board) #print the board
            break
            


def placeShips(board, shipSizes, ai_player=False): #places multiple ships on the board
    for i, size in enumerate(shipSizes): #loop through ships
        print("\nCurrent board:")
        printBoard(board) # Print the empty board before placing ships
        placeShipOnBoard(board, size, f"S{i+1}", ai_player) #place each ship
        events.clear_terminal()


def allShipsSunk(shipHits): #checks if all ships are sunk
    return all(hit == 0 for hit in shipHits.values()) #return True if all ships are sunk
