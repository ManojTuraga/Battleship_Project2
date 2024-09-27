from bullet import *

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

def placeShipOnBoard(board, size, shipId): #places a ship on the board
    while True: #loop
        col, row = getCoordinatesInput() #get coordinates
        orientation = input("Enter H (Horizontal) or V (Vertical): ").strip().upper()#get orientation

        if orientation == 'H': #horizontal placement
            if col + size > boardSize or any(board[row][col + i] != '~' for i in range(size)): #check fit and availability
                print("Invalid placement. Try again.") #invalid placement message
                continue #continue asking
            for i in range(size): #loop through board
                board[row][col + i] = shipId #place ship horizontally
            
            print("\nCurrent board:")# show board
            printBoard(board) #print the board
            break
        elif orientation == 'V': #vertical placement
            if row + size > boardSize or any(board[row + i][col] != '~' for i in range(size)): #check fit and availability
                print("Invalid placement. Try again.") #invalid placement message
                continue #continue asking
            for i in range(size): #loop through board
                board[row + i][col] = shipId #place ship vertically
            
            print("\nCurrent board:")# show board
            printBoard(board) #print the board
            break
        else:
            print("Invalid orientation. Try again.") #if orientation is invalid

def placeShips(board, shipSizes): #places multiple ships on the board
    print("\nCurrent board:")
    printBoard(board) # Print the empty board before placing ships
    for i, size in enumerate(shipSizes): #loop through ships
        placeShipOnBoard(board, size, f"S{i+1}") #place each ship

def checkHitOrMiss(board, row, col): #checks if an attack is a hit or miss
    if board[row][col].startswith("S"): #hit detected
        shipId = board[row][col] #get ship ID
        board[row][col] = "X" #mark hit
        return True, shipId #return hit and ship ID
    board[row][col] = "O" #mark miss
    return False, None #return miss

def allShipsSunk(shipHits): #checks if all ships are sunk
    return all(hit == 0 for hit in shipHits.values()) #return True if all ships are sunk

def playerTurn(opponentBoard, opponentShips, playerTrackingBoard): #handles a player's turn
    print("Your turn to shoot.") #prompt player's turn
    while True: #loop until attack
        col, row = getCoordinatesInput() #get attack coordinates

        opponentBoard, playerTrackingBoard, opponentShips, got_hit, got_sink, hits, sinks = test_bullet.shoot(enemy_board=opponentBoard, knowledge_board=playerTrackingBoard, aim_coordinates = [col, row], opponentShips=opponentShips)
        break #end turn

def setupGame(): #sets up the game
    while True: #loop
        numShips = input("Enter number of ships (1-5): ").strip() #ask for number of ships
        if numShips.isdigit() and 1 <= int(numShips) <= 5: #check if valid input
            numShips = int(numShips) #convert to integer
            break
        print("Invalid number. Try again.") #invalid number message

    #You choose bullets after the number ships
    #I dont want any dumb games of the bullets you getting influencing the ship count
    player1_magazine, player2_magazine = run_draft()

    playerBoard = createEmptyBoard() #create player 1 board
    opponentBoard = createEmptyBoard() #create player 2 board

    print("Player 1, place your ships.") #prompt player 1 to place ships
    placeShips(playerBoard, shipSizes[numShips]) #place player 1's ships

    print("Player 2, place your ships.") #prompt player 2 to place ships
    placeShips(opponentBoard, shipSizes[numShips]) #place player 2's ships

    playerTrackingBoard = createEmptyBoard() #create tracking board for player 1
    opponentTrackingBoard = createEmptyBoard() #create tracking board for player 2

    playerShips = {f"S{i+1}": shipSizes[numShips][i] for i in range(numShips)} #track player ship health
    opponentShips = {f"S{i+1}": shipSizes[numShips][i] for i in range(numShips)} #track opponent ship health

    return playerBoard, opponentBoard, playerTrackingBoard, opponentTrackingBoard, playerShips, opponentShips #return setup

def main(): #main
    print("Welcome to Battleship!") #welcome
    
    playerBoard, opponentBoard, playerTrackingBoard, opponentTrackingBoard, playerShips, opponentShips = setupGame() #setup the game

    while True: #game loop
        print("\nPlayer 1's turn.") #player 1's turn
        print("Your board")
        printBoard(playerBoard) #show player 1's board
        print("Your board")
        printBoard(playerTrackingBoard) #show player 1's tracking board
        playerTurn(opponentBoard, opponentShips, playerTrackingBoard) #player 1 attacks
        if allShipsSunk(opponentShips): #check if player 2's ships are sunk
            print("Player 1 wins!") #player 1 wins
            break #stop the loop

        print("\nPlayer 2's turn.") #player 2's turn
        print("Your board")
        printBoard(opponentBoard) #show player 2's board
        print("Your board")

        printBoard(opponentTrackingBoard) #show player 2's tracking board
        playerTurn(playerBoard, playerShips, opponentTrackingBoard) #player 2 attacks
        if allShipsSunk(playerShips): #check if player 1's ships are sunk
            print("Player 2 wins!") #player 2 wins
            break #stahp

#ok, here will eventually be the function to generate a random bullet.
#it will be used to make the random choices.
#for now, we need it to return basic bullet or test bullet at random.
def randomBullet():
    if random.randint(0,1) == 0:
        return test_bullet
    
    return basic_bullet

#we will also define a function that is repsonsible for the overall "draft" part of the game.
#it is run at the start of main
def run_draft():
    #first, we generate the pool of 12 bullets
    bullet_pool = []
    for i in range(12):
        bullet_pool.append(randomBullet())

    #now, we set up variables to allow players to pick them
    player_1_bullets = []
    player_2_bullets = []
    turn = 1
    picks = 1

    #display the bullet list
    print("Available Bullets:")
    print(str(bullet_pool)) #TODO fancy me
    print("Press enter to continue.")
    input("> ")

    #take turns picking ammo until 2 remain. They are discarded. Lets the players know.
    print("Take turns picking bullets until 2 remain, which will be discarded.")

    while len(bullet_pool) > 2:
        print("Player", str(turn), "turn.")
        print("Picks left this turn:", str(picks))
        print("Available Bullets:")
        print(str(bullet_pool)) #TODO fancy me

        bullet_choice = None
        print("Choose one.")
        while bullet_choice == None:
            temp = int(input("> "))
            if temp < 0 or temp >= len(bullet_pool):
                print("Invalid choice, try again.")

            else:
                bullet_choice = temp

        #now, remove that bullet from the pool and add it to the player's pool
        if turn == 1:
            player_1_bullets.append(bullet_pool[bullet_choice])

        else:
            player_2_bullets.append(bullet_pool[bullet_choice])

        bullet_pool.remove(bullet_pool[bullet_choice])

        #progress the turn
        picks -= 1
        if picks == 0:
            turn %= 2
            turn += 1
            # a special helper to make UI better for last choice
            if len(bullet_pool) == 3:
                picks = 1

            else:
                picks = 2

    #return the lists gotten this way.
    return player_1_bullets, player_2_bullets

if __name__ == "__main__":
    #Bullets used for testing purposes

    main()
