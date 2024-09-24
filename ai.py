import random
import battleship

USED_COORDS = set()

# Medium AI
STACK = []
SHIP_HIT = False 

# Hard AI
OPPONENT_LOCATION = []
    
    
def generateAICoords(is_setup=False):
    while True:
        row = random.choice([i for i in range(battleship.boardSize)])
        col = random.choice([j for j in range(battleship.boardSize)])
        
        if is_setup:
            direction = random.choice(["H", "V"])
            return (row, col, direction)

        if (row, col) not in USED_COORDS:
            USED_COORDS.add((row, col))
            return (row, col)


def stack_directions(row, col):
    possible_directions = choose_direction(row, col)
    
    for i in range(len(possible_directions)):
        possible_directions[i] = next_location(possible_directions[i], row, col)
        
    STACK.extend(possible_directions)
    
    

def determine_ai_player():
    ai_player, difficulty = False, None 
    
    while True:
        ai_player = input("Do you want to play against an AI? (Y/N): ").strip()
        if ai_player in ["Y", "y", "yes"]:
            ai_player = True
            
            diff_hash = {"1" : 1, "Easy" : 1, "easy" : 1, 
                         "2" : 2, "Medium" : 2, "medium" : 2, 
                         "3" : 3, "Hard" : 3, "hard" : 3}
            while True:
                difficulty = input("Select Ai difficulty:\n1) Easy\n2) Medium\n3) Hard\n-> ").strip()
                if difficulty in diff_hash.keys():
                    difficulty = diff_hash[difficulty]
                    break
                print("Invalid input.")
            
            break
        
        elif ai_player in ["N", "n", "no"]:
            ai_player = False 
            break
        
        print("Invalid input.")
    
    return (ai_player, difficulty)


def next_location(direction, row, col):
    
    if direction == "W":
        return (row, col - 1)
    elif direction == "S":
        return (row + 1, col)
    elif direction == "E":
        return (row, col + 1)
    elif direction == "N":
        return (row - 1, col)


def choose_direction(row, col):
    possible_directions = ["N", "E", "S", "W"]
    
    if row + 1 >= battleship.boardSize or (row + 1, col) in USED_COORDS:
        possible_directions.remove("S")
    
    if col + 1 >= battleship.boardSize or (row, col + 1) in USED_COORDS:
        possible_directions.remove("E")
        
    if row - 1 < 0 or (row - 1, col) in USED_COORDS:
        possible_directions.remove("N")
    
    if col - 1 < 0 or (row, col - 1) in USED_COORDS:
        possible_directions.remove("W")
        
    return possible_directions
        
    
    