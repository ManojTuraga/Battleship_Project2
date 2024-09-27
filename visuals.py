from bullet import *

class Visuals:
    def __init__(self, board):
        self.board = board

    def update_board_with_bullet(self, bullet, start_x, start_y):
        hit_pattern = bullet.hit_pattern
        for i, row in enumerate(hit_pattern):
            for j, char in enumerate(row):
                if char == 'X':  # X marks a hit
                    target_x = start_x + i
                    target_y = start_y + j
                    if 0 <= target_x < len(self.board) and 0 <= target_y < len(self.board[0]):
                        self.board[target_x][target_y] = 'X'  # Mark hit
                elif char == 'O':  # O marks a miss
                    target_x = start_x + i
                    target_y = start_y + j
                    if 0 <= target_x < len(self.board) and 0 <= target_y < len(self.board[0]):
                        self.board[target_x][target_y] = 'O'  # Mark miss
        return self.board
    
    def display_bullet_types(self):
        print()
        print("Available Bullets:")
        all_bullets = [standard_bullet] + all_special_bullet_list
        for bullet in all_bullets:
            print()
            self.display_bullet(bullet)

        #more padding.
        print()

    #A small added function to encapsulate the functionality of printing the stuff from a single bullet.
    def display_bullet(self, bullet_in):
        print("-----------------------------")
        print(f"Bullet Name: {bullet_in.name}")
        print(f"Description: {bullet_in.flavor_text}")
        #build a string of the displayed bullet hit pattern
        display_string = "Hit Pattern: \n"

        for row in bullet_in.hit_pattern:
            display_string += "  " + " ".join(str(row)) + "\n"

        print(display_string)
        print("-----------------------------")

    #this came up a few times, so I decided to just make a helper function to print it out.
    def display_hit_pattern_info(self):
        print("Hit pattern key:")
        print("The center of the pattern is where you aimed at.")
        print("~ means nothing is done to that cell.")
        print("X means that cell is attacked.")
        print("O means that cell is revealed.")
        print("A random 'A' cell in each pattern is attacked.")
        print("A random 'B' cell in each pattern is attacked.")
