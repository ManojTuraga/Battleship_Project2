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

        if playerTrackingBoard[row][col] != '~': #check if already attacked
            print("You've already fired at this location. Try again.") #already attacked message
            continue #continue asking

        hit, shipId = checkHitOrMiss(opponentBoard, row, col) #check if hit
        if hit:
            print("It's a hit!") #notify hit
            opponentShips[shipId] -= 1 #reduce ship's health
            playerTrackingBoard[row][col] = "X" #mark hit on tracking board
            if opponentShips[shipId] == 0: #if ship sunk
                print(f"You sunk the opponent's {shipId}!") #notify ship sunk
        else:
            print("It's a miss.") #notify miss
            playerTrackingBoard[row][col] = "O" #mark miss
        break #end turn

def setupGame(): #sets up the game
    while True: #loop
        numShips = input("Enter number of ships (1-5): ").strip() #ask for number of ships
        if numShips.isdigit() and 1 <= int(numShips) <= 5: #check if valid input
            numShips = int(numShips) #convert to integer
            break
        print("Invalid number. Try again.") #invalid number message

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

if __name__ == "__main__":
    main()
