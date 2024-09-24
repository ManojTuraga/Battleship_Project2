'''
Date
Sept 11, 2024

Program Name
Battleship.py

Description
A python program that runs a battleship game.

Inputs
* Number of ships (int)
* Ship Coordinates (str)
* Ship Orientation (str)
* Attack Coordinates (str)

Outputs
* Board Display (str)
* Prompts (str)
* Feedback on Actions (str)
* Sunk Ship Announcements (str)
* Victory Message (str)

Authors / Members
* Abinav Krishnan
* Ansh Rajput
* Liv Sutton
* Ojas Patil
* Priyatam Nuney

'''
import ai
import os
import platform 
from bullet import *
from visuals import Visuals
from scoreboard import *

boardSize = 10 #make the board 10x10
letters = "ABCDEFGHIJ" #string that contains column labels

shipSizes = {  # dictionary for ship sizes based on amount
    1: [1], #ships of size 1 for 1 ship
    2: [1, 2], #ships of size 1 and 2 for 2 ships
    3: [1, 2, 3], #ships of size 1, 2, and 3 for 3 ships
    4: [1, 2, 3, 4], #ships of size 1, 2, 3, 4 for 4 ships
    5: [1, 2, 3, 4, 5] #ships of size 1, 2, 3, 4, and 5 for 5 ships
}


def printBoard(board): #prints the board with row and column labels
    print("  " + " ".join(letters)) #print column labels
    for i in range(boardSize): #loop through rows
        row = [str(cell) for cell in board[i]] #convert cells to strings
        print(f"{i + 1:2} {' '.join(row)}") #print row number and cells


def createEmptyBoard(): #creates a blank board
    return [['~'] * boardSize for _ in range(boardSize)] #fill board with waves (~)


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

        if orientation == 'H': #horizontal placement
            if col + size > boardSize or any(board[row][col + i] != '~' for i in range(size)): #check fit and availability
                if not ai_player: print("Invalid placement. Try again.") #invalid placement message
                continue #continue asking
            for i in range(size): #loop through board
                if not ai_player:  ai.OPPONENT_LOCATION.append((row, col+i))
                board[row][col + i] = shipId #place ship horizontally
            
            print("\nCurrent board:")# show board
            printBoard(board) #print the board
            break
        elif orientation == 'V': #vertical placement
            if row + size > boardSize or any(board[row + i][col] != '~' for i in range(size)): #check fit and availability
                if not ai_player: print("Invalid placement. Try again.") #invalid placement message
                continue #continue asking
            for i in range(size): #loop through board
                if not ai_player: ai.OPPONENT_LOCATION.append((row+i, col))
                board[row + i][col] = shipId #place ship vertically
            
            print("\nCurrent board:")# show board
            printBoard(board) #print the board
            break
        else:
            if not ai_player: print("Invalid orientation. Try again.") #if orientation is invalid


def placeShips(board, shipSizes, ai_player=False): #places multiple ships on the board
    print("\nCurrent board:")
    printBoard(board) # Print the empty board before placing ships
    for i, size in enumerate(shipSizes): #loop through ships
        placeShipOnBoard(board, size, f"S{i+1}", ai_player) #place each ship


def allShipsSunk(shipHits): #checks if all ships are sunk
    return all(hit == 0 for hit in shipHits.values()) #return True if all ships are sunk


def playerTurn(opponentBoard, opponentShips, playerTrackingBoard, ai_player=False, difficulty=None): #handles a player's turn
    print("Your turn to shoot.") #prompt player's turn
    while True: #loop until attack
        
        if ai_player and difficulty == 1:
            row, col = ai.generateAICoords()
            
        elif ai_player and difficulty == 2:
            if ai.SHIP_HIT:
                row, col = ai.STACK.pop()
                ai.USED_COORDS.add((row, col))
            else:
                row, col = ai.generateAICoords()
                
        elif ai_player and difficulty == 3:
            row, col = ai.OPPONENT_LOCATION.pop()
            
        else:
            col, row = getCoordinatesInput() #get attack coordinates

        if playerTrackingBoard[row][col] != '~': #check if already attacked
            if not ai_player: print("You've already fired at this location. Try again.") #already attacked message
            continue #continue asking

        newOpponentBoard, newPlayerTrackingBoard, opponentShips, got_hit, got_sink, hits, sinks = test_bullet.shoot(enemy_board=opponentBoard, knowledge_board=playerTrackingBoard, aim_coordinates = [col, row], opponentShips=opponentShips)

        for i in range( len( newOpponentBoard ) ):
            for j in range( len( newOpponentBoard ) ):
                opponentBoard[ i ][ j ] = newOpponentBoard[ i ][ j ]

        for i in range( len( newPlayerTrackingBoard ) ):
            for j in range( len( newPlayerTrackingBoard ) ):
                playerTrackingBoard[ i ][ j ] = newPlayerTrackingBoard[ i ][ j ]

        if got_hit:            
            print("It's a hit!") #notify hit
            ai.SHIP_HIT = True

            if ai_player:
                for ship_hits in hits.values():
                    for row, col in ship_hits:
                        ai.stack_directions(row, col)
            
            if got_sink: #if ship sunk
                ai.SHIP_HIT = False
                ai.STACK = []

                for ship in sinks:
                    print(f"You sunk the opponent's {ship}!") #notify ship sunk
        else:
            print("It's a miss.") #notify miss
        
        break #end turn
    

def setupGame(): #sets up the game
    while True: #loop
        numShips = input("Enter number of ships (1-5): ").strip() #ask for number of ships
        if numShips.isdigit() and 1 <= int(numShips) <= 5: #check if valid input
            numShips = int(numShips) #convert to integer
            break
        print("Invalid number. Try again.") #invalid number message
        
    ai_player, difficulty = ai.determine_ai_player()
        
    playerBoard = createEmptyBoard() #create player 1 board
    opponentBoard = createEmptyBoard() #create player 2 board

    print("Player 1, place your ships.") #prompt player 1 to place ships
    placeShips(playerBoard, shipSizes[numShips]) #place player 1's ships

    print("Player 2, place your ships.") #prompt player 2 to place ships
    placeShips(opponentBoard, shipSizes[numShips], ai_player) #place player 2's ships

    playerTrackingBoard = createEmptyBoard() #create tracking board for player 1
    opponentTrackingBoard = createEmptyBoard() #create tracking board for player 2

    playerShips = {f"S{i+1}": shipSizes[numShips][i] for i in range(numShips)} #track player ship health
    opponentShips = {f"S{i+1}": shipSizes[numShips][i] for i in range(numShips)} #track opponent ship health

    return playerBoard, opponentBoard, playerTrackingBoard, opponentTrackingBoard, playerShips, opponentShips, ai_player, difficulty #return setup


def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def start_game(scoreboard): # start game
    #print("Welcome to Battleship!") #welcome
    
    playerBoard, opponentBoard, playerTrackingBoard, opponentTrackingBoard, playerShips, opponentShips, ai_player, difficulty = setupGame() #setup the game

    while True: #game loop
        print("\nPlayer 1's turn.") #player 1's turn
        print("Your board")
        printBoard(playerBoard) #show player 1's board
        print("Your board")
        printBoard(playerTrackingBoard) #show player 1's tracking board
        playerTurn(opponentBoard, opponentShips, playerTrackingBoard) #player 1 attacks
        if allShipsSunk(opponentShips): #check if player 2's ships are sunk
            print("Player 1 wins!") #player 1 wins
            scoreboard.update_winner("Player 1") #give point to player 1
            break #stop the loop

        print("\nPlayer 2's turn.") #player 2's turn
        print("Your board")
        printBoard(opponentBoard) #show player 2's board
        print("Your board")

        printBoard(opponentTrackingBoard) #show player 2's tracking board
        playerTurn(playerBoard, playerShips, opponentTrackingBoard, ai_player, difficulty) #player 2 attacks
        if allShipsSunk(playerShips): #check if player 1's ships are sunk
            print("Player 2 wins!") #player 2 wins
            scoreboard.update_winner("Player 2") #give player 2 point
            break #stahp

    #display scoreboard after the game ends
    scoreboard.display_scores()

    #ask if the players want to play again
    while True:
        play_again = input("Do you want to play again? (y/n): ").strip().lower()
        if play_again == 'y':
            clear_terminal()
            return True  #start a new game
        elif play_again == 'n':
            print("Thanks for playing!")
            return False  #exit the game
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

def main(): #main
    scoreboard = Scoreboard()  #initialize scoreboard
    visuals = Visuals(None)  #create an instance of visuals
    
    while True:
        #opening choices/main menu
        print("Welcome to Battleship!")
        print("1. View Bullet Types")
        print("2. Play Game")
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            visuals.display_bullet_types()  #call the method on the visuals instance
            input("\nPress Enter to return to the main menu...")  #have user press enter to go to main menu
        
        elif choice == "2":
            if not start_game(scoreboard):  #if players choose not to play again, end the program
                break
        
        else:
            print("Invalid option. Try again.")  

if __name__ == "__main__":
    main()
