class GameStats():
    def __init__(self, my_settings):
        self.my_settings = my_settings
        self.reset_stats()
        self.game_active = False
        # 在任何情况下都不应充值最高得分
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.my_settings.ship_limit
        self.score = 0
        self.level = 1
