'''
Module: main.py
Creation Date: September 25th, 2024
Author: Manoj Turaga
Contributors: Team 19 Devs, Manoj Turaga, Connor Forristal, Henry Marshall,
              Ceres Botkin, Clare Channel

Description:
    This is the main launching point of the battleship game

Inputs:
    User Inputs
Outputs:
    Transformations on the console state

Sources: W3Schools
'''

# NOTE: We note that the use of eval() was derived from logic in W3Schools.
# We are listing it here so that we don't have to say it every single time we
# use it

###############################################################################
# Imports
###############################################################################
import events
import scoreboard

import visuals
import ai
import board_util
import bullet
import random

###############################################################################
# Procedures
###############################################################################
def random_bullet():
    """
    Function: Random Bullet

    Description: This function is helper that returns a random special bullet

    Inputs: None
    Outputs: random bullet
    """
    # Generate a random list of special bullets based on all tihe special bullets
    # that are supported and return an element in the list

    selected_bullet = bullet.all_special_bullet_list[ random.randint( 0, len( bullet.all_special_bullet_list) - 1 ) ]
    return selected_bullet

def display_bullet_info( params ):
    """
    Function: Random Bullet

    Description: This function is a helper function that displays information
                 about the bullets to the console, whether it be all the bullets
                 or just the bullets in a players magazine

    Inputs: Player Magazine, should clear terminal, is it the opponent, trigger a wait
    Outputs: None
    """
    # Get the visuals, magazine, and whether the terminal should be cleared
    # from the parameters dictionary
    visuals_ = params[ "visuals" ]
    magazine = params[ "magazine" ]
    should_clear_terminal = params[ "should_clear_terminal" ]
    
    is_opp = None
    wait_for_confirmation = False

    # If there is wait for confirmation parameter
    # Get it from the parameters
    if "wait" in params.keys():
        wait_for_confirmation = params[ "wait" ]

    # If there is an is_opp flag in the parameters, get it
    if "is_opp" in params.keys():
        is_opp = params[ "is_opp" ]

    # Clear the terminal when necessary
    if should_clear_terminal:
        events.clear_terminal()

    # If the magazine is None, we will just print out all the
    # information surrounding all the possible bullets
    if magazine == None:
        visuals_.display_bullet_types()
        visuals_.display_hit_pattern_info()

    else:
        # Print whether the magazine is your magazine or the opponent's magazine
        if is_opp is not None:
            if is_opp:
                print( f"The following are the opponent's bullets:" )
            else:
                print( f"The following are your bullets:" )

            print()

        # If the magainze is empty, indicate that there are no bullets
        # in the magazine
        if magazine == []:
            events.display_messages( [ "(None.)" ], False )

        else:
            # For every bullet in the magainze, print the information
            # about the  bullet to the console
            for i in range(len(magazine)):
                print( f"Bullet {i}:" )
                visuals_.display_bullet(bullet_in=magazine[i])
                print()

    # If a wait for confirmation is needed, trigger a wait
    if wait_for_confirmation:
        events.trigger_player_selection( None, [], "Press enter to continue:", False, False )

def run_draft( player1_ai = False, player2_ai = False, player1_difficulty = None, player2_difficulty = None ):
    """
    Function: Run Draft

    Description: This function runs a snake style draft of special bullets
                 between the two players. Players can pick n bullets from
                 a set of random special bullets to aid them in their battle

    Inputs: Whether each player is an AI and their difficulty level
    Outputs: Magazines for Player1 and Player2
    """
    # Initalize a set of 8 random bullets
    bullet_pool = [ random_bullet() for i in range( 8 ) ]

    # Intialize the magazines for player1 and 2, along with the turn
    # of the player and the number of picks remaining
    player1_bullets = []
    player2_bullets = []
    turn = 1
    picks = 1

    visuals_ = visuals.Visuals( None )

    # Initally display all the bullets that can be drafted
    display_bullet_info( { "visuals": visuals_, "magazine": bullet_pool, "should_clear_terminal": True } )
    events.trigger_player_selection( None, [], "Press enter to continue:", False, False )
    events.clear_terminal()

    is_invalid_input = False
    bullet_choice = None

    # The loop will execute until all the bullets that are
    # to be drafted are drafted
    while len( bullet_pool ) > 2:
        events.display_messages( [ "Take turns picking bullets until 2 remain, which will be discarded\n" ], True )
        events.display_messages( [ f"PLAYER {turn} TURN." ], False )

        if eval( "player" + str( turn ) + "_ai" ) == False:
            # If the current player is not an AI, that means the player is allowed to
            # pick a bullet manually. Keep looping until the selection is valid and
            # utlimately set the bullet choice once it is valid
            display_bullet_info( { "visuals": visuals_, "magazine": bullet_pool, "should_clear_terminal": False } )
            bullet_choice = events.trigger_player_selection( f"Picks left this turn: { picks }", [], "Choose one, using the numeric ID of the bullet: ", is_invalid_input, False )
            
            if bullet_choice is None or not bullet_choice.isdigit() or int( bullet_choice ) < 0 or int( bullet_choice ) >= len( bullet_pool ):
                is_invalid_input = True
                continue

            else:
                is_invalid_input = False
                bullet_choice = bullet_pool[ int( bullet_choice ) ]

        else:
            # If the player is an AI, use the the lambda expression in
            # the mapping as a way for the AI to pick the bullet to use.
            # the function to use is based on the difficulty of the AI
            selection_mapping = \
                {
                1: lambda x: min( x, key= lambda y: y.rank ),
                2: lambda x: random.choice( x ),
                3: lambda x: max( x, key= lambda y: y.rank ),
                }
            
            diff = eval( "player" + str(turn) + "_difficulty" )
            
            bullet_choice = selection_mapping[ diff ]( bullet_pool )
        
        # Add the bullet to the player magazine and remove it from the 
        # the bullet pool
        eval( "player" + str(turn) + "_bullets" ).append( bullet_choice )
        bullet_pool.remove( bullet_choice )

        # Display what bullet the player picked and prompt for a continue
        events.display_messages( [ f"Player { turn } chose { bullet_choice.name }" ], False )
        events.trigger_player_selection( None, [], "Press enter to continue:", False, False )
        
        # Decrement the picks and shift the turn
        # when there is no longer any picks that can be made
        picks -= 1
        if picks == 0:
            turn = ( turn % 2 ) + 1
            picks = min( 2, len( bullet_pool ) - 2 )

    return player1_bullets, player2_bullets    

def setup_game( params ):
    """
    Function: Setup Game

    Description: This function does the initalization for the game

    Inputs: If the terminal should be cleared, user input

    Outputs: Initialized instances of board related structures
    """
    should_clear_terminal = params[ "should_clear_terminal" ]

    is_input_invalid = False

    # Loop until all the user selections are vlaid
    while True:
        # Determine the number of ships that the player(s) want to play with
        num_of_ships = events.trigger_player_selection( None, [], "Enter number of ships (1-5): ", is_input_invalid, should_clear_terminal )

        if num_of_ships is None or not num_of_ships.isdigit() or not ( 1 <= int( num_of_ships ) <= 5 ):
            # The following condition is triggered only if the input is invalid
            is_input_invalid = True

        else:
            # Convert the number of ships to an integer
            num_of_ships = int( num_of_ships )

            # Determine if the player is playing with an AI
            # how hard the AI is
            ai_player, difficulty = ai.determine_ai_player()
            events.clear_terminal()

            # Initialize Board Related Structures for player1
            # and player2
            player1_board = board_util.createEmptyBoard()
            player2_tracking_board = board_util.createEmptyBoard()
            player2_board = board_util.createEmptyBoard()
            player1_tracking_board = board_util.createEmptyBoard()

            # Draft the special bullets 
            player1_bullets, player2_bullets = run_draft( player1_ai = False, player2_ai = ai_player, player2_difficulty = difficulty )
            events.clear_terminal()

            # Ask Player 1 to place their ships
            events.display_messages( [ f"Player 1 place your ships" ], True )
            board_util.placeShips( player1_board, board_util.shipSizes[ num_of_ships ] )
            events.clear_terminal()

            # Ask Player 2 to place their ships
            events.display_messages( [ f"Player 2 place your ships" ], True )
            board_util.placeShips( player2_board, board_util.shipSizes[ num_of_ships ], ai_player )
            events.clear_terminal()
            
            # Initialize a structure to store the health of a player's ships
            player1_ship_health = { f"S{ i + 1 }": i + 1 for i in range( num_of_ships ) }
            player2_ship_health = { f"S{ i + 1 }": i + 1 for i in range( num_of_ships ) }

            return player1_board, player1_ship_health, player2_tracking_board, player1_bullets, player2_board, player2_ship_health, player1_tracking_board, player2_bullets, ai_player, difficulty
        
def make_attack( params ):
    """
    Function: Make Attack

    Description: This function executes an attack on the opponents board

    Inputs: Opponent Board related info, player tracking related info, whether a
            special attack is being executed, if the player is an AI and how hard is it

    Outputs: Prints to console
    """
    # Initialize variables to store the bullet and the row and column
    # of the attack
    bullet_ = None
    row = None
    col = None

    # Unpack the parameters from the params dictionary
    opponent_board = params[ "opponent_board" ]
    opponent_ship_health = params[ "opponent_ship_health" ]
    player_tracking_board = params[ "player_tracking_board" ]
    magazine = params[ "magazine" ]
    is_special = params[ "is_special" ]
    ai_player = params[ "ai_player" ]
    difficulty = params[ "difficulty" ]

    status_message = ""

    # This mapping is used by the AI to determine which
    # bullet to use in the magazine, with level 1 being
    # the lowest rank, level 2 being random, and level 3
    # beign the highest ranked bullet
    selection_mapping = \
        {
        1: lambda x: min( x, key= lambda y: y.rank ),
        2: lambda x: random.choice( x ),
        3: lambda x: max( x, key= lambda y: y.rank ),
        }

    if not is_special:
        # If we are not doing a special attack, just use the standard bullet
        bullet_ = bullet.standard_bullet

    if len( magazine ) == 0 and is_special:
        # If the player has no special bullets, don't accept this move and just go back
        # to the calling function
        if not ai_player:
            events.trigger_player_selection( "No Special Bullets to use", None, "Press enter to continue:", False, False )
        return ( False, "" )
    
    else:
        # The following loop is to determine what the location of the
        # attack is and the special bullets that are to be used, if it is
        # a special attack
        while True:
            if not ai_player:
                # If this not an AI player and is a special, determine the bullet that the player
                # wants to use and keep looping until the selection is valid
                if is_special:
                    bullet_ = events.trigger_player_selection( "Select Special Bullet to use", [ b.name for b in magazine ], "Selection: ", False, False )

                    if bullet_ is None or not bullet_.isdigit() or int( bullet_ ) < 1 or int( bullet_ ) > len( magazine ):
                        events.display_messages( [ "Error! Invalid Selection" ], False )
                        continue
                    else:
                        bullet_ = magazine[ int( bullet_ ) - 1 ]

                # Get the coordinates of attack from the user                        
                col, row = board_util.getCoordinatesInput()
                break

            else:
                # If it is an AI, determine the bullet to use from the
                # magazine
                if is_special:
                    bullet_ = selection_mapping[ difficulty ]( magazine )

                # If the AI has difficulty of 1, just generate random coordinates
                if difficulty == 1:
                    row, col = ai.generateAICoords()
                
                # If the AI has difficulty of 2, remove the top of the stack until
                # it can't, then just use random coordinates
                elif difficulty == 2:
                    if ai.SHIP_HIT:
                        row, col = ai.STACK.pop()

                    else:
                        row, col = ai.generateAICoords()

                # If the AI has difficulty of 3, remove the top of the 
                # opponent location stack and use that
                elif difficulty == 3:
                    row, col = ai.OPPONENT_LOCATION.pop()
                break
        
        # If we are executing a special attack, remove it from the magazine
        if is_special:
            magazine.remove( bullet_ )

    # Use the bullet's shoot method on the opponent board
    new_opponent_board, new_player_tracking_board, new_opponent_ships, got_hit, got_sink, hits, sinks = bullet_.shoot(enemy_board=opponent_board, knowledge_board=player_tracking_board, aim_coordinates = [col, row], opponentShips=opponent_ship_health)
    
    # The following 3 for loops are necessary to update the global board
    # information with the information from shoot, to make sure that
    # all important data is copied over
    for i in range( len( new_opponent_board ) ):
        for j in range( len( new_opponent_board ) ):
            opponent_board[ i ][ j ] = new_opponent_board[ i ][ j ]

    for i in range( len( new_player_tracking_board ) ):
        for j in range( len( new_player_tracking_board ) ):
            player_tracking_board[ i ][ j ] = new_player_tracking_board[ i ][ j ]
        
    for key in opponent_ship_health.keys():
        opponent_ship_health[ key ] = new_opponent_ships[ key ]

    # Update the status message with that shot
    status_message += f"Opponent used { bullet_.name } on { board_util.letters[ col ] }{ row + 1 }"

    if got_hit:
        # Update the status message with a hit state and print it to the
        # console if the player is not an AI
        if not ai_player:
            events.display_messages( [ "It's a hit!" ], False )
        
        status_message += "\nIt's a hit!"

        if ai_player:
            # If the player is an AI, indicate that a ship was hit and add
            # it to the stack of coordinates to hit. If we find that the
            # hit did not acutally hit the ship and just revealed, we instead
            # add the coordinate to the stack as well. If the attack hit more
            # than one coordinate, remove it from the stack and the opponent
            # locations and add it to the used coords
            ai.SHIP_HIT = True
            for ship_hits in hits.values():
                for row, col in ship_hits:
                    ai.stack_directions(row, col)

                    if opponent_board[ row ][ col ] == "X":
                        if ( row, col ) in ai.OPPONENT_LOCATION:
                            ai.OPPONENT_LOCATION.remove( ( row, col ) )
                            ai.USED_COORDS.add( ( row, col ) )

                        if ( row, col ) in ai.STACK:
                            ai.STACK.remove( ( row, col ) )
                            ai.USED_COORDS.add( ( row, col ) )

                    else:
                        ai.STACK.append( ( row, col ) )

                    if len( ai.STACK ) == 0:
                        ai.SHIP_HIT = False
    
        if got_sink: #if ship sunk
            # If the player sunk a ship, reset the state of the AI if the player
            # is an AI and display all the ships that were sunk as both a status
            # message and printed to the console (if the player is not an AI)
            if ai_player:
                ai.SHIP_HIT = False
                ai.STACK = []

            for ship in sinks:
                if not ai_player:
                    events.display_messages( [ f"You sunk the opponent's {ship}!" ], False )
                status_message += f"\nYour {ship} was sunk"
    else:
        # The attack missed, so update the status message and print the
        # status back to the user if the player is not an AI
        if not ai_player:
            events.display_messages( [ f"It's a miss" ], False )
        status_message += "\nIt's a miss"

    return ( True, status_message )

    
        
def player_turn( opponent_board, opponent_ship_health, player_board, player_tracking_board, ai_player = False, difficulty = None, player_no = "-1", magazine = [], oppponent_magazine = [], status_message = None ):
    """
    Function: Player Turn

    Description: This function determines and exectues what a player does in a turn. this includes making attacks,
                 getting information, and/or conceding

    Inputs: User Inputs for different selections, the opponent board and ship health, the player board
            the player tracking board, if the player is an AI, how difficult is the AI, player ID, player magazine,
            the opponent magazine, and any statuses that need to be displayed

    Outputs: Prints to console
    """
    visuals_ = visuals.Visuals( None )

    # Loop until an input requires that the turn ends
    while True:
        # Initialize a list of all the options that a player can do
        # on their turn
        selected_turn_option = None
        turn_options = ["Attack Normally",
                        "Use Special Bullet",
                        "Look at your Bullets", 
                        "Look at opponent's Bullets", 
                        "Display all Special Bullet Info", 
                        "Concede"]
        
        # Create a mapping between turn selections and the functions that they
        # call, with their parameters
        turn_options_maps = \
            {
            1 : { "func": make_attack, "params": { "opponent_board" : opponent_board, "opponent_ship_health" : opponent_ship_health, "player_tracking_board" : player_tracking_board, 
                                                  "magazine" : magazine, "is_special" : False, "ai_player" : ai_player, "difficulty" : difficulty } },
            2 : { "func": make_attack, "params": { "opponent_board" : opponent_board, "opponent_ship_health" : opponent_ship_health, "player_tracking_board" : player_tracking_board, 
                                                  "magazine" : magazine, "is_special" : True, "ai_player" : ai_player, "difficulty" : difficulty } },
            3 : { "func": display_bullet_info, "params": { "should_clear_terminal" : True, "is_opp" : False, "visuals" : visuals_, "wait" : True, "magazine" : magazine } },
            4 : { "func": display_bullet_info, "params": { "should_clear_terminal" : True, "is_opp" : True, "visuals" : visuals_, "wait" : True, "magazine" : oppponent_magazine } },
            5 : { "func": display_bullet_info, "params": { "should_clear_terminal" : True, "is_opp" : True, "visuals" : visuals_, "wait" : True, "magazine" : None } },
            6 : { "func": lambda x : ( True, "conceded" ), "params": {} }
            }
        
        is_invalid_option = False

        # Loop until the selected turn is valid. This code
        # is only executed if a player is not an AI
        while selected_turn_option == None and not ai_player:
            # Print both the player's tracking board and the player board
            # to the console
            events.clear_terminal()
            events.display_messages( [ f"Player { player_no } turn." ], False )
        
            events.display_messages( [ f"Opponent's Board." ], False )
            board_util.printBoard( player_tracking_board )
            events.display_messages( [ "" ], False )

            events.display_messages( [ f"Your Board." ], False )
            board_util.printBoard( player_board )
            events.display_messages( [ "" ], False )

            # If there is a status message and the current player is
            # not an AI, print the status message
            if status_message is not None and not ai_player:
                events.display_messages( [ status_message + '\n' ], False )

            # Determine what the player wants to do
            selected_turn_option = events.trigger_player_selection( "Options", turn_options, "What do you wish to do: ", is_invalid_option, False )

            if selected_turn_option == None or not selected_turn_option.isdigit() or int( selected_turn_option ) < 1 or int( selected_turn_option ) > len( turn_options ):
                # The following code is triggered if the selection was invalid
                is_invalid_option = True
                selected_turn_option = None

            else:
                # Convert the selection into an integer
                selected_turn_option = int( selected_turn_option )

        if ai_player:
            # If the player is an AI, if the AI can select a special bullet
            # there is a 25 * difficulty chance that it uses the special
            # bullet. Otherwise, the AI will just do a normal attack
            if len( magazine ) > 0 and random.randint( 0, 100 ) <= 25 * difficulty:
                selected_turn_option = 2
            else:
                selected_turn_option = 1

        # Execute the function corresponding to the selection
        val = turn_options_maps[ selected_turn_option ][ "func" ]( turn_options_maps[ selected_turn_option ][ "params" ] )

        # If the turn needs to end, return the status message corresponding
        # to it
        if selected_turn_option not in [ 3, 4, 5 ] and val[ 0 ]:
            return val[ 1 ]
        
        events.clear_terminal()
        

def play_game( params ):
    """
    Function: Play Game

    Description: This function is the launching point for actually playing
                 the game. A player can start an instance of the game without
                 actually playing, so this is why this is not the launching point

    Inputs: User Inputs for different selections
    Outputs: Prints to console
    """
    # Determine player1 and player2 ships, tracks, magazine, and
    # any AI related ancillary data
    player1_board, player1_ship_health, player2_tracking_board, player1_bullets, player2_board, player2_ship_health, player1_tracking_board, player2_bullets, ai_player, difficulty = setup_game( params )

    # Create a mapping of player id and board information
    # for easy access
    board_mapping = \
        {
        '1': { "player board": player1_board, "player tracking board": player2_tracking_board, "player ships": player1_ship_health, "player magazine": player1_bullets, 
               "opponent board": player2_board, "opponent tracking board": player1_tracking_board, "opponent ships": player2_ship_health, "opponent magazine": player2_bullets },
        '2': { "player board": player2_board, "player tracking board": player1_tracking_board, "player ships": player2_ship_health, "player magazine": player2_bullets, 
               "opponent board": player1_board, "opponent tracking board": player2_tracking_board, "opponent ships": player1_ship_health, "opponent magazine": player1_bullets }
        }
    
    # Initialize variables to store the ID of the curent player and the 
    # opponent. Also create a variable to determine if the current player is an AI
    cur_player = '1'
    op_player = '2'
    is_ai = False

    status_message = None
    
    # We loop until a player conceeds or a winner is determined
    while True:
        # Clear the terminal and get access to the opponent board data, as
        # well as the player tracking board and any bullet related information
        events.clear_terminal()
        opponent_board_ref = board_mapping[ cur_player ][ "opponent board" ]
        opponent_ships_ref = board_mapping[ cur_player ][ "opponent ships" ]
        player_board_ref = board_mapping[ cur_player ][ "player board" ]
        player_tracking_board_ref = board_mapping[ cur_player ][ "player tracking board" ]
        magazine_ref = board_mapping[ cur_player ][ "player magazine" ]
        opponent_magazine_ref = board_mapping[ cur_player ][ "opponent magazine" ]

        # Execute the player's turn
        val = player_turn( opponent_board_ref, opponent_ships_ref, player_board_ref, player_tracking_board_ref, is_ai, difficulty, cur_player, magazine_ref, opponent_magazine_ref, status_message )

        if val == "conceded":
            # If the current player conceded, indicate that the other player is the
            # winner
            return op_player
        
        status_message = val

        if board_util.allShipsSunk( opponent_ships_ref ):
            # If a player destroyed all of their opponent's ships in their
            # turn, that player is the winner
            return cur_player
        
        if not is_ai:
            # The AI doesn't have to wait for anybody, so only display
            # a wait message when needed to transfer the machine
            events.trigger_player_selection( f"Player {cur_player}, press enter when you want your turn to end. This will clear the console, so look at things before that.", [], "> ", False, False )
            events.clear_terminal()

        # A player is an AI if the result of XORing the
        # state of the AI with whether the opponent is an AI
        # is True
        is_ai = is_ai ^ ai_player

        if not is_ai:
            # Same reasoning as previous not is_ai check
            events.trigger_player_selection( f"Waiting for player {op_player}. Player {op_player}, press enter to start turn.", [], "> ", False, False )
            events.clear_terminal()

        # Switch the player IDs
        temp = cur_player
        cur_player = op_player
        op_player = temp



def game_loop():
    """
    Function: Game Loop

    Description: This function is the main game loop of the battleship game.
                 The game loop is composed of getting information about what
                 is composed in the game and actually starting the game

    Inputs: User Inputs for different selections
    Outputs: Prints to console
    """
    # Create variables to store information about this page.
    # This page is just mainly responsible for fetching information
    # about bullets and actually starting the game
    initial_msg = "Welcome to Battleship!"
    list_of_start_options = [ "View Bullet Types", "Play Game" ]
    selection_msg = "Choose an option: "
    trigger_maps = { "1": display_bullet_info, "2": play_game }

    # Initalize an instance of the visuals class
    visuals_ = visuals.Visuals( None )

    # Initialize the function parameters with the instance of the
    # visuals class and indicate that the terminal should be cleared
    # on every print and there is no magazine to print
    function_params = dict()
    function_params[ "visuals" ] = visuals_
    function_params[ "should_clear_terminal" ] = True
    function_params[ "magazine" ] = None

    is_input_invalid = False

    # Keep looping until a winner is determined
    while True:
        # Determine if the player wants to play or see information
        # about the bullets
        option = events.trigger_player_selection( initial_msg, list_of_start_options, selection_msg, is_input_invalid, True )

        if option not in trigger_maps.keys():
            # This condition is only triggered if the input is invalid
            is_input_invalid = True

        else:
            # Call the corersponding procedure based on the input
            winner = trigger_maps[ option ]( function_params )

            if option == "1":
                # If the user wanted to see the bullets, only proceed with the loop
                # once the get pass the continue prompt
                events.trigger_player_selection( None, [], "Press enter to continue:", False, False )

            if option == "2":
                # Return the ID of the winner back to the calling function
                return winner

def main():
    """
    Function: Main

    Description: This function is the launching point of the entire program

    Inputs: None
    Outputs: None
    """
    # Initialize an instance of the scoreboard and hold a flag to
    # determine if the input is invalid or not
    score = scoreboard.Scoreboard()
    is_input_invalid = False

    # We will have a loop to make sure that the game keeps running
    # until the player no long wants to keep playing
    while True:
        # Start the main game loop
        winner = game_loop()

        # Update the scoreboard with the winner of the the game
        # and display the scores to the console
        score.update_winner( f"Player { winner }" )
        events.display_messages( [ f"Player { winner } wins" ], True )
        score.display_scores()

        # Ask the player if they want to play again
        choice = events.trigger_player_selection( None, [], "Do you want to play again (y/n)? ", is_input_invalid, False )

        if choice not in [ 'Y', 'y', 'N', 'n' ]:
            # This condition is only triggered if the input is invalid
            is_input_invalid = True

        else:
            # Reset the AI if the prompt is valid, regardless of whether
            # they want to keep playing or not
            ai.STACK.clear()
            ai.USED_COORDS = set()
            ai.OPPONENT_LOCATION.clear()
            ai.SHIP_HIT = False
            
            # If the player no longer wants to keep playing, end the game
            if choice.lower() == 'n':
                events.display_messages( [ "Thanks for playing!" ], False )
                break


# Only call the main function if this module
# is being called directly
if __name__ == "__main__":
    main()