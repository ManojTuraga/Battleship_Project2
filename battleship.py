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
* Priyatam NuneyS

'''
import ai
from bullet import *
from visuals import Visuals
from scoreboard import *
from board_util import *

def display_bullets( visuals_, magazine ):
    if magazine == []:
        print("(None.)")

    else:
        for i in range(len(magazine)):
            print( f"Bullet {i}:" )
            visuals_.display_bullet(bullet_in=magazine[i])
            print()

def get_user_confirmation():
    print("Press enter to continue.")
    input("> ")


def playerTurn(opponentBoard, opponentShips, playerBoard, playerTrackingBoard, ai_player=False, difficulty=None, player_no="-1", magazine = [], opponent_magazine = []): #handles a player's turn
    #make a visuals object to help with this
    visuals_ = Visuals(None)

    while True: #loop until done
        print("Player", player_no, "turn.") #prompt player's turn

        print("Opponent's board:")
        printBoard(playerTrackingBoard)
        print()

        print("Your board:")
        printBoard(playerBoard)
        print()
        
        #now, we have to offer the player some options.
        #I want to offer looking at your own magazine, looking at the opponent's, conceding, attacking normally, or using a speical bullet.
        #oh also seeing hit pattern info.
        #so, I guess offer a choice from a pool of those options?
        selected_turn_option = None
        turn_options = ["Attack Normally",
                        "Use Special Bullet",
                        "Look at your Bullets", 
                        "Look at opponent's Bullets", 
                        "See hit Pattern Info", 
                        "Concede"]
        
        while selected_turn_option == None and ai_player == False:
            for i in range(len(turn_options)):
                print(str(i) + "-", turn_options[i])
            
            print("What do you wish to do?")
            player_choice_attempt = input(">")
            try:
                selected_turn_option = turn_options[int(player_choice_attempt)]

            except:
                print("Invalid input, try again.")
                print()

        if ai_player:
            #this is a special area where the AI decides what to do.
            #first, it looks at it's magazine. If empty, it just attacks, as it cannot do anything other than that.
            if len(magazine) == 0:
                selected_turn_option = "Attack Normally"

            #if not, it can attack normally or use a special bullet, depending on difficulty. I am saying +25% per difficulty level
            elif random.randint(0, 100) <= 25 * difficulty:
                selected_turn_option = "Use Special Bullet"

            #otherwise, just attack normally.
            else:
                selected_turn_option = "Attack Normally"

        ##OK, from here downwards will be the different turn actions area
        if selected_turn_option == "Concede":
            #ask the player if they really want to.
            #also, AI can never do this so we do not need to worry about them here.
            clear_terminal()
            print("Do you really want to concede? (y/n)")
            while True:
                player_concede = input("> ")
                if player_concede.lower() == "y":
                    print("Conceding now.")
                    return "Conceded"
                elif player_concede.lower() == "n":
                    print("Aborting Concession.")
                    break
                else:
                    print("Invalid input, Try again.")

        elif selected_turn_option == "Look at your Bullets":
            #show the bullets that you have
            clear_terminal()
            print("The following are the bullets you have currently:")

            display_bullets( visuals_, magazine )

            #wait until confirmation to exit, while the player looks at this.
            print("Press enter to continue.")
            input("> ")
            clear_terminal()

        elif selected_turn_option == "Look at opponent's Bullets":
            #show the opponent's bullets.
            clear_terminal()
            print("The following are the bullets your opponent has currently:")

            display_bullets( visuals_, opponent_magazine )

            #wait until confirmation to exit, while the player looks at this.
            get_user_confirmation()
            clear_terminal()

        elif selected_turn_option == "See hit Pattern Info":
            #show the player the info on hit patterns, for if they forget.
            clear_terminal()
            visuals_.display_hit_pattern_info()

            print()

            #wait until confirmation to exit, while the player looks at this.
            get_user_confirmation()
            clear_terminal()

        elif selected_turn_option == "Use Special Bullet":
            #a catcher for if a player with no bullets left tries to use this.
            if len(magazine) == 0:
                print("You don't have any special bullets left to use, try another option!")
                continue
            
            ai_selection_func = None

            #shoot a special bullet.
            if ai_player:
                #ai player area
                if difficulty == 1:
                    #easy ai area.
                    #they will always fire thier lowest-rank bullet first.
                    lowest_rank = None
                    for i in range(len(magazine)):
                        if lowest_rank == None or lowest_rank > magazine[i].rank:
                            lowest_rank = magazine[i].rank

                    for i in range(len(magazine)):
                        if magazine[i].rank == lowest_rank:
                            break

                    #now, i will be equal to the index of the bullet in your magazine that you want to use.
                    
                    row, col = ai.generateAICoords()

                    #ok, we have the location and the bullet at this point.

                    #shooting will be done down below, in the area common to all AIs

                elif difficulty == 2:
                    #medium ai area.
                    #they will always fire one of their bullets at random.
                    i = random.randint(0, len(magazine) - 1)

                    #now, i will be equal to the index of the bullet in your magazine that you want to use.
                    
                    if ai.SHIP_HIT:
                        row, col = ai.STACK.pop()
                        ai.USED_COORDS.add((row, col))
                    else:
                        row, col = ai.generateAICoords()

                    #ok, we have the location and the bullet at this point.

                    #shooting will be done down below, in the area common to all AIs

                elif difficulty == 3:
                    #hard ai area.
                    #they will always fire their highest-rank bullets first.
                    highest_rank = None
                    for i in range(len(magazine)):
                        if highest_rank == None or highest_rank < magazine[i].rank:
                            highest_rank = magazine[i].rank

                    for i in range(len(magazine)):
                        if magazine[i].rank == highest_rank:
                            break

                    #now, i will be equal to the index of the bullet in your magazine that you want to use.

                    row, col = ai.OPPONENT_LOCATION.pop()

                    #ok, we have the location and the bullet at this point.

                    #shooting will be done down below, in the area common to all AIs

                #shoot it
                newOpponentBoard, newPlayerTrackingBoard, opponentShips, got_hit, got_sink, hits, sinks = magazine[i].shoot(enemy_board=opponentBoard, knowledge_board=playerTrackingBoard, aim_coordinates = [col, row], opponentShips=opponentShips)
                #remove it from the magazine.
                magazine.remove(magazine[i])

                #TODO
                #Tell the player about the effects of the bullet being shot, update the information within the AI
                #update the board given the effects of the bullet that we now know.

                #end your turn
                break

            else:
                #human player area.
                #first, display all of the bullets to the player for them to select one of them.
                for i in range(len(magazine)):
                    print( f"Bullet {i}:" )
                    visuals_.display_bullet(bullet_in=magazine[i])
                    print()

                #Select one
                print("Select one of the above bullets you have, using the number associated with it.")
                while True:
                    player_bullet_choice = input("> ")
                    try:
                        temp = magazine[int(player_bullet_choice)]

                        #looks like the bullet choice was valid if temp worked, so we can save the choice int and exit the loop
                        player_bullet_choice = int(player_bullet_choice)

                        break

                    except:
                        #must have been invalid. Get the player to try again.
                        print("Invalid choice. Try again.")

                #now we have the choice, so get the coordinates to shoot the bullet at.

                col, row = getCoordinatesInput()
                
                #now, shoot the bullet.
                newOpponentBoard, newPlayerTrackingBoard, opponentShips, got_hit, got_sink, hits, sinks = magazine[player_bullet_choice].shoot(enemy_board=opponentBoard, knowledge_board=playerTrackingBoard, aim_coordinates = [col, row], opponentShips=opponentShips)

                for i in range( len( newOpponentBoard ) ):
                    for j in range( len( newOpponentBoard ) ):
                        opponentBoard[ i ][ j ] = newOpponentBoard[ i ][ j ]

                for i in range( len( newPlayerTrackingBoard ) ):
                    for j in range( len( newPlayerTrackingBoard ) ):
                        playerTrackingBoard[ i ][ j ] = newPlayerTrackingBoard[ i ][ j ]

                #remove it from your magazine.
                magazine.remove(magazine[player_bullet_choice])
                break

        elif selected_turn_option == "Attack Normally":
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

            newOpponentBoard, newPlayerTrackingBoard, opponentShips, got_hit, got_sink, hits, sinks = standard_bullet.shoot(enemy_board=opponentBoard, knowledge_board=playerTrackingBoard, aim_coordinates = [col, row], opponentShips=opponentShips)

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
    clear_terminal()
        
    playerBoard = createEmptyBoard() #create player 1 board
    opponentBoard = createEmptyBoard() #create player 2 board

    #Now, we make the players each select their bullets.
    player1_magazine, player2_magazine = run_draft(player1_ai= False, player1_difficulty= None, player2_ai= ai_player, player2_difficulty= difficulty)
    clear_terminal()

    print("Player 1, place your ships.") #prompt player 1 to place ships
    placeShips(playerBoard, shipSizes[numShips]) #place player 1's ships
    clear_terminal()

    print("Player 2, place your ships.") #prompt player 2 to place ships
    placeShips(opponentBoard, shipSizes[numShips], ai_player) #place player 2's ships
    clear_terminal()

    playerTrackingBoard = createEmptyBoard() #create tracking board for player 1
    opponentTrackingBoard = createEmptyBoard() #create tracking board for player 2

    playerShips = {f"S{i+1}": shipSizes[numShips][i] for i in range(numShips)} #track player ship health
    opponentShips = {f"S{i+1}": shipSizes[numShips][i] for i in range(numShips)} #track opponent ship health

    return playerBoard, opponentBoard, playerTrackingBoard, opponentTrackingBoard, playerShips, opponentShips, ai_player, difficulty, player1_magazine, player2_magazine #return setup


#return a random bullet, to be used to generate the draft pool.
def randomBullet():
    selected_bullet = all_special_bullet_list[random.randint(0, len(all_special_bullet_list) - 1)]

    return selected_bullet

#we will also define a function that is repsonsible for the overall "draft" part of the game.
#it is run at the start of main
#it takes in a bool for if each player is AI or not, and difficulty for each player if they are AI.
def run_draft(player1_ai = False, player2_ai = False, player1_difficulty = None, player2_difficulty = None):
    #first, we generate the pool of 8 bullets
    bullet_pool = []
    for i in range(8):
        bullet_pool.append(randomBullet())

    #now, we set up variables to allow players to pick them
    player_1_bullets = []
    player_2_bullets = []
    turn = 1
    picks = 1

    #display the bullet list
    #make a visuals object to help with this
    visuals_ = Visuals(None)
    print("Available Bullets:\n")
    for i in range(len(bullet_pool)):
        print(f"Bullet {i}: ")
        visuals_.display_bullet(bullet_in=bullet_pool[i])
        print()
    print("Press enter to continue.")
    input("> ")
    clear_terminal()
    
    while len(bullet_pool) > 2:
        #take turns picking ammo until 2 remain. They are discarded. Lets the players know.
        clear_terminal()
        print("Take turns picking bullets until 2 remain, which will be discarded.\n")

        if eval("player" + str(turn) + "_ai") == False:
            #only show this sort of thing to players
            print("Available Bullets:\n")
            for i in range(len(bullet_pool)):
                print(f"Bullet {i}: ")
                visuals_.display_bullet(bullet_in=bullet_pool[i])
                print()

        print("PLAYER", str(turn), "TURN.") #in caps so that the players hopefully do not accidentally pick for one another.

        if eval("player" + str(turn) + "_ai") == False:
            #human player selector area.
            print("Picks left this turn:", str(picks))
            print("Choose one, using the numeric ID of the bullet.")

            bullet_choice = None
            while bullet_choice == None:
                try:
                    temp = int(input("> "))
                except:
                    continue
                
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

        else:
            #ai player bullet selector area.
            diff = eval("player" + str(turn) + "_difficulty")
            if diff == 1:
                #easy AI area
                #their method is to find the lowest rank among bullets available, and pick the first bullet of that rank
                lowest_rank = None
                for bullet_ in bullet_pool:
                    if lowest_rank == None or bullet_.rank < lowest_rank:
                        lowest_rank = bullet_.rank

                #go through to find the choice
                for i in range(len(bullet_pool)):
                    if bullet_pool[i].rank == lowest_rank:
                        #choose this! 
                        #copy the name for display, add it to the pool the remove is from the list.
                        chosen_bullet_name = bullet_pool[i].name
                        if turn == 1:
                            player_1_bullets.append(bullet_pool[i])

                        else:
                            player_2_bullets.append(bullet_pool[i])

                        bullet_pool.remove(bullet_pool[i])
                        break

            elif diff == 2:
                #medium AI area
                #this AI just selects a bullet at random
                i = random.randint(0, len(bullet_pool) - 1)
                chosen_bullet_name = bullet_pool[i].name
                if turn == 1:
                    player_1_bullets.append(bullet_pool[i])

                else:
                    player_2_bullets.append(bullet_pool[i])

                bullet_pool.remove(bullet_pool[i])

            elif diff == 3:
                #hard AI area
                #their method is to find the highest rank among bullets available, and pick the first bullet of that rank
                highest_rank = None
                for bullet_ in bullet_pool:
                    if highest_rank == None or bullet_.rank > highest_rank:
                        highest_rank = bullet_.rank

                #go through to find the choice
                for i in range(len(bullet_pool)):
                    if bullet_pool[i].rank == highest_rank:
                        #choose this! 
                        #copy the name for display, add it to the pool the remove is from the list.
                        chosen_bullet_name = bullet_pool[i].name
                        if turn == 1:
                            player_1_bullets.append(bullet_pool[i])

                        else:
                            player_2_bullets.append(bullet_pool[i])

                        bullet_pool.remove(bullet_pool[i])
                        break

            #print out choice to opponent
            print("Player", str(turn), "chose", chosen_bullet_name + ".")

            print("Press enter to continue.") #this is so the player can better see what is going on.
            input("> ")


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

def start_game(scoreboard): # start game
    #print("Welcome to Battleship!") #welcome
    
    playerBoard, opponentBoard, playerTrackingBoard, opponentTrackingBoard, playerShips, opponentShips, ai_player, difficulty, player1_magazine, player2_magazine = setupGame() #setup the game
    
    board_mapping = \
        {
        '1': { "player board": playerBoard, "player tracking board": playerTrackingBoard, "player ships": playerShips, "player magazine": player1_magazine, 
               "opponent board": opponentBoard, "opponent tracking board": opponentTrackingBoard, "opponent ships": opponentShips, "opponent magazine": player2_magazine },
        '2': { "player board": opponentBoard, "player tracking board": opponentTrackingBoard, "player ships": opponentShips, "player magazine": player2_magazine, 
               "opponent board": playerBoard, "opponent tracking board": playerTrackingBoard, "opponent ships": playerShips, "opponent magazine": player1_magazine }
        }
    
    cur_player = '1'
    op_player = '2'

    while True: #game loop
        clear_terminal()
        opponentBoardRef = board_mapping[ cur_player ][ "opponent board" ]
        opponentShipsRef = board_mapping[ cur_player ][ "opponent ships" ]
        playerBoardRef = board_mapping[ cur_player ][ "player board" ]
        magazineRef = board_mapping[ cur_player ][ "player magazine" ]
        opponentMagazineRef = board_mapping[ cur_player ][ "opponent magazine" ]

        concede_maybe = playerTurn(opponentBoardRef, opponentShipsRef, playerBoardRef, playerTrackingBoard, player_no=cur_player, magazine = magazineRef, opponent_magazine=opponentMagazineRef) #player 1 attacks

        #check for a concession
        if concede_maybe == "Conceded":
            print(f"Player {op_player} wins!")
            scoreboard.update_winner(f"Player {op_player}") #give point to player 1
            break #stop the loop

        if allShipsSunk(opponentShips): #check if player 2's ships are sunk
            print(f"Player {cur_player} wins!") #player 1 wins
            scoreboard.update_winner(f"Player {cur_player}") #give point to player 1
            break #stop the loop

        #this allows the hotseat mechanism to work a lot better, so no seeing the other player's board.
        if not ai_player:
            print(f"Player {cur_player}, press enter when you want your turn to end. This will clear the console, so look at things before that.")
            input("> ")
            clear_terminal()
            print(f"Waiting for player {op_player}. Player {op_player}, press enter to start turn.")
            input("> ")
            clear_terminal()

        temp = cur_player
        cur_player = op_player
        op_player = temp

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
        clear_terminal()
        print("Welcome to Battleship!")
        print("1. View Bullet Types")
        print("2. Play Game")
        choice = input("Choose an option: ").strip()
        
        if choice == "1":
            clear_terminal()
            visuals.display_bullet_types()  #call the method on the visuals instance
            visuals.display_hit_pattern_info() #for player info
            input("\nPress Enter to return to the main menu...")  #have user press enter to go to main menu
        
        elif choice == "2":
            clear_terminal()
            if not start_game(scoreboard):  #if players choose not to play again, end the program
                break
        
        else:
            print("Invalid option. Try again.")  

if __name__ == "__main__":
    main()
