import pygame as pg
from vector import Vector
from pygame.sprite import Sprite, Group
from copy import copy
from random import randint
from timer import CommandTimer
# from alien import Alien
# from stats import Stats


class Barriers:
    def __init__(self, game, ul):
        self.game = game
        self.settings = game.settings
        self.barriers = Group()
        self.ul_list = [(ul[0] + 240 * n, ul[1]) for n in range(5)]
        for point in self.ul_list:
            self.create_barrier(game=game, ul=point)

    def update(self):
        for barrier in self.barriers:
            barrier.update()

    def draw(self):
        for barrier in self.barriers:
            barrier.draw()

    def create_barrier(self, game, ul):
        barrier = Barrier(game=game, ul=ul, wh=self.settings.barrier_wh)
        self.barriers.add(barrier)


class Barrier(Sprite):
    img_list = [pg.image.load(f'images/wall1_{x+1}.png') for x in range(2)]
    img_list_bl = [pg.image.load(f'images/wall1BL_{x+1}.png') for x in range(2)]
    img_list_br = [pg.image.load(f'images/wall1BR_{x+1}.png') for x in range(2)]
    img_list_tl = [pg.image.load(f'images/wall1TL_{x+1}.png') for x in range(2)]
    img_list_tr = [pg.image.load(f'images/wall1TR_{x+1}.png') for x in range(2)]
    def __init__(self, game, ul, wh):
        super().__init__()
        self.game = game
        self.settings = self.game.settings
        self.alien_fleet = self.game.alien_fleet
        self.barrier_elements = Group()
        self.ul = ul
        self.wh = wh
        self.lasers = self.game.lasers
        self.draw_solid_blocks()

    def update(self):
        laser_collide = pg.sprite.groupcollide(self.barrier_elements,
                        self.lasers.lasers, False, True)
        for be in laser_collide:
            be.hit()

        alien_laser_collide = pg.sprite.groupcollide(self.barrier_elements,
                              self.alien_fleet.lasers.lasers, False, True)

        for be in alien_laser_collide:
            be.hit()

        alien_collide = pg.sprite.groupcollide(self.barrier_elements,
                        self.alien_fleet.fleet, False, False)

        for collision in alien_collide.items():
            be = collision[0]
            aliens = collision[1]
            for alien in aliens:
                if not alien.dying:
                    alien.hit()
                    be.hit()

    def draw(self):
        for be in self.barrier_elements:
            be.draw()

    def draw_solid_blocks(self):
        end = 32 * 3
        for row in range(self.wh[0], self.wh[0] + end, 32):
            for col in range(self.wh[1], self.wh[1] + end, 32):
                if row == self.wh[0] and col == self.wh[1]:
                    be = BarrierElement(game=self.game, img_list=Barrier.img_list_tl,
                        ul=(self.ul[0] + col, self.ul[1] + row), wh=self.settings.barrier_wh)
                elif row == self.wh[0] and col == self.wh[1] + end - 32:
                    be = BarrierElement(game=self.game, img_list=Barrier.img_list_tr,
                        ul=(self.ul[0] + col, self.ul[1] + row), wh=self.settings.barrier_wh)
                else:
                    be = BarrierElement(game=self.game, img_list=Barrier.img_list,
                        ul=(self.ul[0] + col, self.ul[1] + row), wh=self.settings.barrier_wh)
                self.barrier_elements.add(be)

        be = BarrierElement(game=self.game, img_list=Barrier.img_list_br,
            ul=(self.ul[0] + self.wh[1], self.ul[1] + self.wh[0] + end ), wh=self.settings.barrier_wh)
        self.barrier_elements.add(be)
        be = BarrierElement(game=self.game, img_list=Barrier.img_list_bl,
            ul=(self.ul[0] + self.wh[1] + end - 32, self.ul[1] + self.wh[0] + end ), wh=self.settings.barrier_wh)
        self.barrier_elements.add(be)

class BarrierElement(Sprite):
    def __init__(self, game, img_list, ul, wh):
        super().__init__()
        self.ul = ul
        self.wh = wh
        self.rect = pg.Rect(ul[0], ul[1], wh[0], wh[1])
        self.timer = CommandTimer(image_list=img_list, is_loop=False,
                                  start_index=0)
        self.screen = game.screen

    def update(self): pass

    def hit(self):
        self.timer.next_frame()
        if self.timer.is_expired():
            self.kill()

    def draw(self):
        image = self.timer.image()
        rect = image.get_rect()
        rect.x, rect.y = self.rect.x, self.rect.y
        self.screen.blit(image, rect)
