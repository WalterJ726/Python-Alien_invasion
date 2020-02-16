class Settings():
    def __init__(self):
        """初始化游戏的静态设置"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 控制飞船的速度
        self.ship_limit = 3

        # 子弹的设置
        self.bullet_color = 60, 60, 60
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_allowed = 10

        # 控制外星人的速度
        self.fleet_drop_speed = 30

        self.speedup_scale = 1.1
        self.score_scale = 1.5
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleet_direction = 1 为右移
        self.fleet_direction = 1
        # 计分
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        # print(self.alien_points)  击杀一个就多少分
