import sys
import pygame
import time
from settings import Settings
from ship import Ship
from alien import Alien
from button import Button
from scoreboard import Scoreboard
from game_stats import GameStats
import game_functions as gf
from pygame.sprite import Group


def run_game():
    pygame.init()
    my_settings = Settings()
    screen = pygame.display.set_mode((my_settings.screen_width, my_settings.screen_height))
    ship = Ship(my_settings, screen)
    # alien = Alien(my_settings, screen)
    pygame.display.set_caption("alien invasion".title())
    bullets = Group()
    aliens = Group()
    # 创建一个用于存储游戏统计信息的实例
    stats = GameStats(my_settings)
    sb = Scoreboard(my_settings, screen, stats)
    gf.create_fleet(my_settings, screen, ship, aliens)
    # 创建一个按钮实例
    play_button = Button(my_settings, screen, "Play")
    while True:
        gf.check_events(my_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(my_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(my_settings, screen, stats, sb, ship, aliens, bullets)
        # time.sleep(0.01)
        gf.update_screen(my_settings, screen, stats, sb, ship, aliens, bullets, play_button)  # 静态显示，游戏不在活动状态下。在任何时候都会显示


run_game()