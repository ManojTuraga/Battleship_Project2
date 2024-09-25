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
        all_bullets = [
            {'name': 'Test Bullet', 'flavor': 'I am for testing only', 'pattern': 'XBB, AXA, ~O~'},
            {'name': 'Basic Bullet', 'flavor': 'This is your typical one coordinate shot', 'pattern': 'X'}
        ]
        for bullet in all_bullets:
            print()
            print("-----------------------------")
            print(f"Bullet Name: {bullet['name']}")
            print(f"Description: {bullet['flavor']}")
            print(f"Hit Pattern: {bullet['pattern']}")
            print("-----------------------------")
