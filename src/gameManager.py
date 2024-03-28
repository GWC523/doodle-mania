class GameManager:
    def __init__(self):
        self.game_state = 0
        self.score = 0
        self.max_score = 0
        self.lives = 3
        self.alpha = 255
        self.entities_alive = []

    def update_max_score(self, score):
        if score > self.max_score:
            self.max_score = score

    def reset_game(self):
        self.score = 0
        self.lives = 3
        self.alpha = 255
        self.entities_alive = []