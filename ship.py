import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, my_settings, screen):
        # 飞船基本设置
        super().__init__()
        self.my_settings = my_settings

        self.screen = screen
        self.image = pygame.image.load("images/ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 飞船坐标的获得
        self.center = float(self.rect.centerx)
        self.rect.bottom = self.screen_rect.bottom

        # 控制飞船的持续移动
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        # 必须使用两个if，如果一个if，一个elif优先级不一样
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.my_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.my_settings.ship_speed_factor

        # 根据center更新rect对象（飞船的那张图片）
        self.rect.centerx = self.center

    def center_ship(self):
        self.center = self.screen_rect.centerx
