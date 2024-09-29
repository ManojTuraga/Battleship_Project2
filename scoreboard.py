'''
Module: events.py
Creation Date: September 25th, 2024
Author: Clare Channel
Contributors: Clare Channel

Description:
    This module provides the definiton/implementation of the scoreboard
    class, which keeps track of how many times each player has won the
    game

Inputs:
    Winning Player
Outputs:
    Prints the current standings to console

Sources:
'''
###############################################################################
# Types
###############################################################################
# The following is the definition and the implementation of the scoreboard
# class
class Scoreboard:
    def __init__(self):
        """
        Function: Initialization

        Description: This is the initialization function for the scoreboard class

        Inputs: None 
        Outputs: None
        """
        # Initalize a member that stores the player id as keys and the amount
        # of times each player has won
        self.scores = {"Player 1": 0, "Player 2": 0}

    def update_winner(self, winner):
        """
        Function: Update Winner

        Description: This function takes in the winner of the previous game and
                     updates the number of times they have won.

        Inputs: Winner 
        Outputs: None
        """
        # If the winner ID is in the scores member of this class, update the count
        # of the ID by one
        if winner in self.scores:
            self.scores[winner] += 1

    def display_scores(self):
        """
        Function: Display Scores

        Description: This function takes the information stored in the class members
                     and prints them to the console

        Inputs: None
        Outputs: Prints to console
        """
        # Essentially, take the contents of the scores dictionary
        # and print it to the console
        print("\nScoreboard:")
        for player, score in self.scores.items():
            print(f"{player}: {score} wins")
