class Scoreboard:
    def __init__(self):
        self.scores = {"Player 1": 0, "Player 2": 0}

    def update_winner(self, winner):
        if winner in self.scores:
            self.scores[winner] += 1

    def display_scores(self):
        print("\nScoreboard:")
        for player, score in self.scores.items():
            print(f"{player}: {score} wins")

    def reset_scores(self):
        self.scores = {"Player 1": 0, "Player 2": 0}
