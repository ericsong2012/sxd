import sys

import pygame

from bullet import Bullet

from alien import Alien

from time import sleep

def check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets,sb):
    #监视键盘和鼠标事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,ship,aliens,bullets,stats,play_button,mouse_x,mouse_y,sb)

def check_play_button(ai_settings,screen,ship,aliens,bullets,stats,play_button,mouse_x,mouse_y,sb):
    """在玩家点击Play按钮时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        stats.reset_stats()
         #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        stats.game_active = True
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        #隐藏光标
        pygame.mouse.set_visible(False)
        #重置游戏信息
        game_reset(ai_settings,screen,ship,aliens,bullets)

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    if event.key == pygame.K_LEFT:
        ship.move_left = True
    if event.key == pygame.K_SPACE:
       fire_bullet(ai_settings,screen,ship,bullets)
    if event.key == pygame.K_q:
            sys.exit()

def fire_bullet(ai_settings,screen,ship,bullets):
    """创建一颗子弹，并加入的编组中"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    if event.key == pygame.K_LEFT:
        ship.move_left = False

def update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button,sb):
    screen.fill(ai_settings.bg_color)
    #在飞船和外星人后面重绘所有子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    #让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(bullets):
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets,stats,sb):
     collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
     if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)

     if len(aliens) == 0:
        bullets.empty()
        #加快游戏节奏
        ai_settings.increase_speed()
        create_fleet(ai_settings,screen,ship,aliens)
        #升级
        stats.level += 1
        sb.prep_level()

def check_high_score(stats,sb):
    """检查是否诞生了最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

def create_fleet(ai_settings,screen,ship,aliens):
    """创建外星人编组"""
    #创建一个外星人，并计算一行可容纳多少个外星人
    #外星人的间距为外星人的宽度
    alien = Alien(ai_settings,screen)
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def get_number_aliens_x(ai_settings,alien_width):
    """计算每行可以容纳多少个外星人"""
    #屏幕中可以容纳外星人的宽度
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings,screen,aliens,alien_number,row_number):
     #创建一个外星人，并且加入当前行
     alien = Alien(ai_settings,screen)
     alien_width = alien.rect.width
     alien.x = alien_width + 2 * alien_width * alien_number
     alien.rect.x = alien.x
     alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
     aliens.add(alien)

def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y = (ai_settings.screen_height -
                                (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def check_fleet_edges(ai_settings,aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    """将整个外星人下移，并改变他们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def update_aliens(ai_settings,screen,stats,ship,aliens,bullets,sb):
    """检查是否有外星人位于屏幕边缘位置，并更新外星人群中所有外星人的位置"""
    check_fleet_edges(ai_settings,aliens)
    aliens.update()
    #检测外星人与飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb)
    #检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings,screen,stats,ship,aliens,bullets)

def ship_hit(ai_settings,stats,screen,ship,aliens,bullets,sb):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        #将ship_left 减1
        stats.ships_left -= 1
        #重置游戏信息
        game_reset(ai_settings,screen,ship,aliens,bullets)
        #更新记分牌
        sb.prep_ships()
        #暂停
        sleep(0.5)
    else:
        stats.game_active = False

def game_reset(ai_settings,screen,ship,aliens,bullets):
    #清空外星人列表和子弹列表
    aliens.empty()
    bullets.empty()
    #创建一群新的外星人，并将飞船放到屏幕底端中央
    create_fleet(ai_settings,screen,ship,aliens)
    ship.center_ship()

def check_aliens_bottom(ai_settings,screen,stats,ship,aliens,bullets):
    """检查是否有外星人到大屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞一样处理
            ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
            break


