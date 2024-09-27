#this is the implementation of the bullet class for our custom bullets
#we need random and the main functions
import random
from battleship import *

#this will be used for every bullet that is implemented
class Bullet:
    def __init__(self, rank= 0, flavor_text = "", hit_pattern = [], name = "Unnamed Bullet"):
        #this is text that can optionally be used in the UI. It comes attached to every bullet
        self.flavor_text = flavor_text

        #the name of the bullet. Nice for the UI to be able to use.
        self.name = name

        #a ranking for each bullet. Smarter AIs will use this to decide which bullets to take, probably.
        self.rank = rank

        #The hit pattern of the bullet.
        self.hit_pattern = hit_pattern

    #a helper function that gets the center of the hit pattern, in coordinates
    def _get_center(self):
        #get X, round it
        x_out = int(len(self.hit_pattern) / 2)

        #get Y, round it
        y_out = int(len(self.hit_pattern) / 2)

        #return a list of them
        return [x_out, y_out]

    #temporary function to help testing
    def __str__(self):
        return self.name

    #a second helper function that resolves all A and Bs into X-s within a pattern
    def _resolve_pattern(self):
        #make a copy of the pattern
        new_pattern = []
        for row in self.hit_pattern:
            new_pattern.append(row[:])

        #now, get a list of all coordinates of each A and B here
        A_list = []
        B_list = []
        for i in range(len(new_pattern[0])):
            for j in range(len(new_pattern)):
                if new_pattern[j][i] == "A":
                    A_list.append([j, i])
                
                elif new_pattern[j][i] == "B":
                    B_list.append([j, i])

        #get a random coordinate from each of those lists, and replace it with X
        if len(A_list) > 0:
            selected_coord = A_list[random.randint(0, len(A_list) - 1)]

            #This is gross, but strings are immutable so it must be done
            new_pattern[selected_coord[0]] = new_pattern[selected_coord[0]][:selected_coord[1]] + "X" + new_pattern[selected_coord[0]][selected_coord[1] + 1:]

        if len(B_list) > 0:
            selected_coord = B_list[random.randint(0, len(B_list) - 1)]

            new_pattern[selected_coord[0]] = new_pattern[selected_coord[0]][:selected_coord[1]] + "X" + new_pattern[selected_coord[0]][selected_coord[1] + 1:]

        #now, we need to replace the rest of the As and Bs with ~s
        for i in range(len(new_pattern)):
            new_pattern[i] = new_pattern[i].replace("A", "~").replace("B", "~")

        #the new pattern is now done, return it.
        return new_pattern
    

    #the last function is one to automatically apply the effect of the bullet to the board
    #it takes the board of the enemy and your representaiton of it and where this is aimed at
    #also, it takes opponentships
    #it returns all boards modified.
    #boards inserted as 2D arrays
    #also will return 2 bools. One of if this shot hit at all.
    #one of if this shot sunk a boat. I think these are needed for AI.
    #also, it returns the ids of the boats it hit or sinks, if any
    def shoot(self, opponentShips = [], aim_coordinates = [0, 0], enemy_board = [], knowledge_board = []):
        #first, we need to get the pattern and center of this bullet.
        
        hit_pattern = self._resolve_pattern()
        offset_coordinates = self._get_center()
        
        #set up some bools
        got_hit = False
        got_sink = False
        hit_ids = []
        sink_ids = []
        
        #now, we iterate through each character of the hit pattern
        for i in range(len(hit_pattern[0])):
            for j in range(len(hit_pattern)):
                #at this point, we are dealing with 3 coordinates.
                #let's simplify those.
                cur_x = i + aim_coordinates[0] - offset_coordinates[0]
                cur_y = j + aim_coordinates[1] - offset_coordinates[1]
                
                #now, we look at where those are. If off the board, skip them.
                if cur_x < 0 or cur_y < 0:
                    continue
                
                elif cur_x >= len(enemy_board[0]) or cur_y >= len(enemy_board):
                    continue
                
                #ok, we are on the map. Now check what type of thing to do.
                if hit_pattern[j][i] == "~":
                    #do nothing.
                    pass
                
                elif hit_pattern[j][i] == "X":
                    #attack this location
                    hit, ship_id = checkHitOrMiss(enemy_board, cur_y, cur_x)
                    
                    if hit:
                        got_hit = True
                        if ship_id not in hit_ids:
                            hit_ids.append(ship_id)
                            
                        opponentShips[ship_id] -= 1 
                        knowledge_board[cur_x][cur_y] = "X" #mark hit on tracking board
                        if opponentShips[ship_id] == 0: #if ship sunk
                            got_sink = True
                            if ship_id not in sink_ids:
                                sink_ids.append(ship_id)
                            
                    else:
                        knowledge_board[cur_y][cur_y] = "O" #mark miss
                
                elif hit_pattern[j][i] == "O":
                    #reveal this location
                    #if the location on the enemy map has a boat
                    #add information to your own map.
                    #also, count as a "hit" for the AI
                    if "~" != enemy_board[cur_y][cur_x]:
                        got_hit = True
                        knowledge_board[cur_y][cur_x] = enemy_board[cur_y][cur_x][:].replace("O", "~")
                        
        return enemy_board, knowledge_board, opponentShips, got_hit, got_sink, hit_ids, sink_ids
        
#Bullets used for testing purposes
test_bullet = Bullet(rank=-2, flavor_text="I am for testing only.", hit_pattern=["XBB", "AXA", "~O~"], name= "Test Bullet")
basic_bullet = Bullet(rank=-1, flavor_text="Basic Shot.", hit_pattern=["X"], name= "Basic Bullet")

