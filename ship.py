import pygame

from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self,ai_settings,screen):
        """初始化飞船并设置其初始化的位置"""

        super(Ship,self).__init__()

        self.screen = screen

        #加载飞船图像并获取其外接矩形
        self.image  = pygame.image.load("images/plan_small.bmp")

        self.image = pygame.transform.scale(self.image,
                    (ai_settings.ship_width,ai_settings.ship_height))
        #获取 飞船的矩形坐标
        self.rect = self.image.get_rect()
        #获取屏幕的矩形坐标
        self.screen_rect = screen.get_rect()

        #将飞船放在屏幕的底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #移动标识
        self.move_right = False
        self.move_left = False

        #移动的速度因子
        self.ship_speed_factor = ai_settings.ship_speed_factor
        #书籍中self.rect.centerx只能存储数值的说法,目前python3已经支持
        self.center = float(self.rect.centerx)

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image,self.rect)

    def update(self):
        """根据移动标识调整飞船的位置"""
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.center += self.ship_speed_factor
        if self.move_left and self.rect.left > 0:
            self.center -= self.ship_speed_factor

        self.rect.centerx = self.center

    def center_ship(self):
        """让飞船在屏幕居中"""
        self.center  = self.screen_rect.centerx


