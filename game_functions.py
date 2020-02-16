import sys
import pygame
import time
from bullet import Bullet
from alien import Alien


def check_keydown_event(event, my_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(my_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_event(event, my_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(my_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, my_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_event(event, my_settings, screen, ship, bullets)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(my_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(my_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        my_settings.initialize_dynamic_settings()
        # 重置游戏统计信息
        stats.reset_stats()  # 为什么这样reset可以成功？
        stats.game_active = True
        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        # 隐藏光标
        pygame.mouse.set_visible(False)
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(my_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    for alien in aliens.sprites():
        alien.blitme()
    sb.show_score()
    # aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(my_settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        check_bullet_alien_collisions(my_settings, screen, stats, sb, ship, aliens, bullets)


def update_aliens(my_settings, screen, stats, sb, ship, aliens, bullets):
    check_fleet_edges(my_settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(my_settings, screen, stats, sb, ship, aliens, bullets)
    check_aliens_bottom(my_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(my_settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += my_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        my_settings.increase_speed()
        create_fleet(my_settings, screen, ship, aliens)
        # 提高等级
        stats.level += 1
        sb.prep_level()


def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def check_fleet_edges(my_settings, aliens):
    for alien in aliens:
        if alien.check_edges():
            change_fleet_direction(my_settings, aliens)
            break


def change_fleet_direction(my_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += my_settings.fleet_drop_speed
    my_settings.fleet_direction *= -1


def ship_hit(my_settings, screen, stats, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

    # 清空外星人和子弹
    aliens.empty()
    bullets.empty()

    # 创建一群新的外星人
    create_fleet(my_settings, screen, ship, aliens)
    ship.center_ship()

    # 暂停
    time.sleep(0.5)


def check_aliens_bottom(my_settings, screen, stats, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(my_settings, screen, stats, sb, ship, aliens, bullets)
            break


def fire_bullet(my_settings, screen, ship, bullets):
    if len(bullets) < my_settings.bullet_allowed:
        new_bullet = Bullet(my_settings, screen, ship)
        bullets.add(new_bullet)


def create_fleet(my_settings, screen, ship, aliens):
    alien = Alien(my_settings, screen)
    number_aliens_x = get_number_aliens_x(my_settings, alien.rect.width)
    number_rows = get_number_rows(my_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(my_settings, screen, aliens, alien_number, row_number)


def get_number_aliens_x(my_settings, alien_width):
    available_space_x = my_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))  # 下取整不会太拥挤
    return number_aliens_x


def get_number_rows(my_settings, ship_height, alien_height):
    available_space_y = (my_settings.screen_height - ship_height - 3 * alien_height)  # 上边距，加上飞船，加上飞船上面有一段距离
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(my_settings, screen, aliens, alien_number, row_number):
    alien = Alien(my_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.y = alien_height + 2 * alien_height * row_number
    alien.rect.x = alien.x
    alien.rect.y = alien.y
    aliens.add(alien)