import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

import game_functions as gf

def run_game():

	#初始化游戏并创建一个屏幕对象
    pygame.init()

    ai_settings = Settings()

    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))

    pygame.display.set_caption("Alien Invasion")

	#创建play 按钮
    play_button = Button(ai_settings,screen,"Play")

	#创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)

    #创建记分牌
    sb = Scoreboard(ai_settings,screen,stats)

    #创建一艘飞船
    ship = Ship(ai_settings,screen)

    #创建一个存储子弹的编组
    bullets = Group()

	#创建外星人编组
    aliens = Group()

    gf.create_fleet(ai_settings,screen,ship,aliens)

    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings,screen,stats,play_button,ship,aliens,bullets,sb)
        if stats.game_active:
            ship.update()
            bullets.update()
            gf.update_bullets(bullets)
            gf.update_aliens(ai_settings,screen,stats,ship,aliens,bullets,sb)
            gf.check_bullet_alien_collisions(ai_settings,screen,ship,aliens,bullets,stats,sb)
        gf.update_screen(ai_settings,screen,stats,ship,aliens,bullets,play_button,sb)

run_game()
