import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):

    def __init__(self, my_settings, screen, ship):
        super().__init__()
        self.screen = screen

        self.rect = pygame.Rect(0, 0, my_settings.bullet_width, my_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 储存子弹的位置用小数来保存
        self.y = float(self.rect.y)

        self.color = my_settings.bullet_color
        self.speed_factor = my_settings.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)