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
    selected_bullet = bullet.all_special_bullet_list[ random.randint( 0, len( bullet.all_special_bullet_list) - 1 ) ]

    return selected_bullet

def display_bullet_info( params ):
    visuals_ = params[ "visuals" ]
    magazine = params[ "magazine" ]
    should_clear_terminal = params[ "should_clear_terminal" ]
    
    is_opp = None
    wait_for_confirmation = False

    if "wait" in params.keys():
        wait_for_confirmation = params[ "wait" ]

    if "is_opp" in params.keys():
        is_opp = params[ "is_opp" ]

    if should_clear_terminal:
        events.clear_terminal()

    if magazine == None:
        visuals_.display_bullet_types()
        visuals_.display_hit_pattern_info()

    else:
        if is_opp is not None:
            if is_opp:
                print( f"The following are the opponent's bullets:" )
            else:
                print( f"The following are your bullets:" )

            print()

        if magazine == []:
            events.display_messages( [ "(None.)" ], False )
            print("(None.)")

        else:
            for i in range(len(magazine)):
                print( f"Bullet {i}:" )
                visuals_.display_bullet(bullet_in=magazine[i])
                print()

    if wait_for_confirmation:
        events.trigger_player_selection( None, [], "Press enter to continue:", False, False )

def run_draft( player1_ai = False, player2_ai = False, player1_difficulty = None, player2_difficulty = None ):
    bullet_pool = [ random_bullet() for i in range( 8 ) ]

    player1_bullets = []
    player2_bullets = []
    turn = 1
    picks = 1

    visuals_ = visuals.Visuals( None )

    display_bullet_info( { "visuals": visuals_, "magazine": bullet_pool, "should_clear_terminal": True } )
    events.trigger_player_selection( None, [], "Press enter to continue:", False, False )
    events.clear_terminal()

    is_invalid_input = False
    bullet_choice = None

    while len( bullet_pool ) > 2:
        events.display_messages( [ "Take turns picking bullets until 2 remain, which will be discarded\n" ], True )
        
        events.display_messages( [ f"PLAYER {turn} TURN." ], False )

        if eval( "player" + str( turn ) + "_ai" ) == False:
            display_bullet_info( { "visuals": visuals_, "magazine": bullet_pool, "should_clear_terminal": False } )
            bullet_choice = events.trigger_player_selection( f"Picks left this turn: { picks }", [], "Choose one, using the numeric ID of the bullet: ", is_invalid_input, False )
            
            if bullet_choice is None or not bullet_choice.isdigit() or int( bullet_choice ) < 0 or int( bullet_choice ) >= len( bullet_pool ):
                is_invalid_input = True
                continue

            else:
                is_invalid_input = False
                bullet_choice = bullet_pool[ int( bullet_choice ) ]

        else:
            selection_mapping = \
                {
                1: lambda x: min( x, key= lambda y: y.rank ),
                2: lambda x: random.choice( x ),
                3: lambda x: max( x, key= lambda y: y.rank ),
                }
            
            diff = eval( "player" + str(turn) + "_difficulty" )
            
            bullet_choice = selection_mapping[ diff ]( bullet_pool )
        
        eval( "player" + str(turn) + "_bullets" ).append( bullet_choice )
        bullet_pool.remove( bullet_choice )

        events.display_messages( [ f"Player { turn } chose { bullet_choice.name }" ], False )
        events.trigger_player_selection( None, [], "Press enter to continue:", False, False )
        
        picks -= 1
        if picks == 0:
            turn = ( turn % 2 ) + 1
            picks = min( 2, len( bullet_pool ) - 2 )

    return player1_bullets, player2_bullets    

def setup_game( params ):
    visuals_ = params[ "visuals" ]
    should_clear_terminal = params[ "should_clear_terminal" ]

    is_input_invalid = False

    while True:
        num_of_ships = events.trigger_player_selection( None, [], "Enter number of ships (1-5): ", is_input_invalid, should_clear_terminal )

        if num_of_ships is None or not num_of_ships.isdigit() or not ( 1 <= int( num_of_ships ) <= 5 ):
            is_input_invalid = True

        else:
            num_of_ships = int( num_of_ships )

            ai_player, difficulty = ai.determine_ai_player()
            events.clear_terminal()

            player1_board = board_util.createEmptyBoard()
            player2_tracking_board = board_util.createEmptyBoard()

            player2_board = board_util.createEmptyBoard()
            player1_tracking_board = board_util.createEmptyBoard()

            player1_bullets, player2_bullets = run_draft( player1_ai = False, player2_ai = ai_player, player2_difficulty = difficulty )
            events.clear_terminal()

            events.display_messages( [ f"Player 1 place your ships" ], True )
            board_util.placeShips( player1_board, board_util.shipSizes[ num_of_ships ] )
            events.clear_terminal()

            events.display_messages( [ f"Player 2 place your ships" ], True )
            board_util.placeShips( player2_board, board_util.shipSizes[ num_of_ships ], ai_player )
            events.clear_terminal()
            
            player1_ship_health = { f"S{ i + 1 }": i + 1 for i in range( num_of_ships ) }
            player2_ship_health = { f"S{ i + 1 }": i + 1 for i in range( num_of_ships ) }

            return player1_board, player1_ship_health, player2_tracking_board, player1_bullets, player2_board, player2_ship_health, player1_tracking_board, player2_bullets, ai_player, difficulty
        
def make_attack( params ):
    bullet_ = None
    row = None
    col = None

    opponent_board = params[ "opponent_board" ]
    opponent_ship_health = params[ "opponent_ship_health" ]
    player_tracking_board = params[ "player_tracking_board" ]
    magazine = params[ "magazine" ]
    is_special = params[ "is_special" ]
    ai_player = params[ "ai_player" ]
    difficulty = params[ "difficulty" ]

    status_message = ""

    selection_mapping = \
        {
        1: lambda x: min( x, key= lambda y: y.rank ),
        2: lambda x: random.choice( x ),
        3: lambda x: max( x, key= lambda y: y.rank ),
        }

    if not is_special:
        bullet_ = bullet.standard_bullet

    if len( magazine ) == 0 and is_special:
        events.trigger_player_selection( "No Special Bullets to use", None, "Press enter to continue:", False, False )
        return ( False, "" )
    
    else:
        while True:
            if not ai_player:
                if is_special:
                    bullet_ = events.trigger_player_selection( "Select Special Bullet to use", [ b.name for b in magazine ], "Selection: ", False, False )

                    if bullet_ is None or not bullet_.isdigit() or int( bullet_ ) < 1 or int( bullet_ ) > len( magazine ):
                        events.display_messages( [ "Error! Invalid Selection" ], False )
                        continue
                    else:
                        bullet_ = magazine[ int( bullet_ ) - 1 ]
                        
                col, row = board_util.getCoordinatesInput()
                break

            else:
                if is_special:
                    bullet_ = selection_mapping[ difficulty ]( magazine )
                if difficulty == 1:
                    row, col = ai.generateAICoords()
                
                elif difficulty == 2:
                    if ai.SHIP_HIT:
                        row, col = ai.STACK.pop()

                    else:
                        row, col = ai.generateAICoords()

                elif difficulty == 3:
                    row, col = ai.OPPONENT_LOCATION.pop()
                break
        
        if is_special:
            magazine.remove( bullet_ )

    new_opponent_board, new_player_tracking_board, new_opponent_ships, got_hit, got_sink, hits, sinks = bullet_.shoot(enemy_board=opponent_board, knowledge_board=player_tracking_board, aim_coordinates = [col, row], opponentShips=opponent_ship_health)
    
    for i in range( len( new_opponent_board ) ):
        for j in range( len( new_opponent_board ) ):
            opponent_board[ i ][ j ] = new_opponent_board[ i ][ j ]

    for i in range( len( new_player_tracking_board ) ):
        for j in range( len( new_player_tracking_board ) ):
            player_tracking_board[ i ][ j ] = new_player_tracking_board[ i ][ j ]
        
    for key in opponent_ship_health.keys():
        opponent_ship_health[ key ] = new_opponent_ships[ key ]

    status_message += f"Opponent used { bullet_.name } on { board_util.letters[ col ] }{ row + 1 }"

    if got_hit:
        if not ai_player:
            events.display_messages( [ "It's a hit!" ], False ) #notify hit
        
        status_message += "\nIt's a hit!"

        if ai_player:
            ai.SHIP_HIT = True
            for ship_hits in hits.values():
                for row, col in ship_hits:
                    ai.stack_directions(row, col)

                    if opponent_board[ row ][ col ] == "X":
                        if ( row, col ) in ai.OPPONENT_LOCATION:
                            ai.OPPONENT_LOCATION.remove( ( row, col ) )

                        if ( row, col ) in ai.STACK:
                            ai.STACK.remove( ( row, col ) )
    
        if got_sink: #if ship sunk
            if ai_player:
                ai.SHIP_HIT = False
                ai.STACK = []

            for ship in sinks:
                if not ai_player:
                    events.display_messages( [ f"You sunk the opponent's {ship}!" ], False )
                status_message += f"\nYour {ship} was sunk"
    else:
        if not ai_player:
            events.display_messages( [ f"It's a miss" ], False )
        status_message += "\nIt's a miss"

    return ( True, status_message )

    
        
def player_turn( opponent_board, opponent_ship_health, player_board, player_tracking_board, ai_player = False, difficulty = None, player_no = "-1", magazine = [], oppponent_magazine = [], status_message = None ):
    visuals_ = visuals.Visuals( None )

    while True:
        selected_turn_option = None
        turn_options = ["Attack Normally",
                        "Use Special Bullet",
                        "Look at your Bullets", 
                        "Look at opponent's Bullets", 
                        "Display all Special Bullet Info", 
                        "Concede"]
        
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
        while selected_turn_option == None and not ai_player:
            events.clear_terminal()
            events.display_messages( [ f"Player { player_no } turn." ], False )
        
            events.display_messages( [ f"Opponent's Board." ], False )
            board_util.printBoard( player_tracking_board )
            events.display_messages( [ "" ], False )

            events.display_messages( [ f"Your Board." ], False )
            board_util.printBoard( player_board )
            events.display_messages( [ "" ], False )

            if status_message is not None and not ai_player:
                events.display_messages( [ status_message + '\n' ], False )

            selected_turn_option = events.trigger_player_selection( "Options", turn_options, "What do you wish to do: ", is_invalid_option, False )

            if selected_turn_option == None or not selected_turn_option.isdigit() or int( selected_turn_option ) < 1 or int( selected_turn_option ) > len( turn_options ):
                is_invalid_option = True
                selected_turn_option = None

            else:
                selected_turn_option = int( selected_turn_option )

        if ai_player:
            if len( magazine ) > 0 and random.randint( 0, 100 ) <= 25 * difficulty:
                selected_turn_option = 2
            else:
                selected_turn_option = 1

        val = turn_options_maps[ selected_turn_option ][ "func" ]( turn_options_maps[ selected_turn_option ][ "params" ] )

        if selected_turn_option not in [ 3, 4, 5 ] and val[ 0 ]:
            return val[ 1 ]
        
        events.clear_terminal()
        

def play_game( params ):
    player1_board, player1_ship_health, player2_tracking_board, player1_bullets, player2_board, player2_ship_health, player1_tracking_board, player2_bullets, ai_player, difficulty = setup_game( params )

    board_mapping = \
        {
        '1': { "player board": player1_board, "player tracking board": player2_tracking_board, "player ships": player1_ship_health, "player magazine": player1_bullets, 
               "opponent board": player2_board, "opponent tracking board": player1_tracking_board, "opponent ships": player2_ship_health, "opponent magazine": player2_bullets },
        '2': { "player board": player2_board, "player tracking board": player1_tracking_board, "player ships": player2_ship_health, "player magazine": player2_bullets, 
               "opponent board": player1_board, "opponent tracking board": player2_tracking_board, "opponent ships": player1_ship_health, "opponent magazine": player1_bullets }
        }
    
    cur_player = '1'
    op_player = '2'
    visuals = params[ "visuals" ]
    is_ai = False

    status_message = None

    while True:
        events.clear_terminal()
        opponent_board_ref = board_mapping[ cur_player ][ "opponent board" ]
        opponent_ships_ref = board_mapping[ cur_player ][ "opponent ships" ]
        player_board_ref = board_mapping[ cur_player ][ "player board" ]
        player_tracking_board_ref = board_mapping[ cur_player ][ "player tracking board" ]
        magazine_ref = board_mapping[ cur_player ][ "player magazine" ]
        opponent_magazine_ref = board_mapping[ cur_player ][ "opponent magazine" ]

        val = player_turn( opponent_board_ref, opponent_ships_ref, player_board_ref, player_tracking_board_ref, is_ai, difficulty, cur_player, magazine_ref, opponent_magazine_ref, status_message )

        if val == "conceded":
            return op_player
        
        status_message = val

        if board_util.allShipsSunk( opponent_ships_ref ):
            return cur_player
        
        if not is_ai:
            events.trigger_player_selection( f"Player {cur_player}, press enter when you want your turn to end. This will clear the console, so look at things before that.", [], "> ", False, False )
            events.clear_terminal()

        is_ai = is_ai ^ ai_player

        if not is_ai:
            events.trigger_player_selection( f"Waiting for player {op_player}. Player {op_player}, press enter to start turn.", [], "> ", False, False )
            events.clear_terminal()

        temp = cur_player
        cur_player = op_player
        op_player = temp



def game_loop():
    initial_msg = "Welcome to Battleship!"
    list_of_start_options = [ "View Bullet Types", "Play Game" ]
    selection_msg = "Choose an option: "
    trigger_maps = { "1": display_bullet_info, "2": play_game }

    visuals_ = visuals.Visuals( None )

    function_params = dict()
    function_params[ "visuals" ] = visuals_
    function_params[ "should_clear_terminal" ] = True
    function_params[ "magazine" ] = None

    is_input_invalid = False

    while True:
        option = events.trigger_player_selection( initial_msg, list_of_start_options, selection_msg, is_input_invalid, True )

        if option not in trigger_maps.keys():
            is_input_invalid = True

        else:
            winner = trigger_maps[ option ]( function_params )

            if option == "1":
                events.trigger_player_selection( None, [], "Press enter to continue:", False, False )

            if option == "2":
                return winner

def main():
    score = scoreboard.Scoreboard()
    is_input_invalid = False

    while True:
        winner = game_loop()

        score.update_winner( f"Player { winner }" )
        events.display_messages( [ f"Player { winner } wins" ], True )
        score.display_scores()

        choice = events.trigger_player_selection( None, [], "Do you want to play again (y/n)? ", is_input_invalid, False )

        if choice not in [ 'Y', 'y', 'N', 'n' ]:
            is_input_invalid = True

        else:
            if choice.lower() == 'n':
                events.display_messages( [ "Thanks for playing!" ], False )
                break


if __name__ == "__main__":
    main()