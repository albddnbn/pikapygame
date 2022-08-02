import pygame
import os

class Background:
    def __init__(self, game):
        self.game = game
        self.settings = self.game.settings
        self.screen = self.game.screen
        self.scroll_speed = self.settings.scroll_speed

        self.bg_image = pygame.image.load('images/city_bg.png')
        self.rect1 = self.bg_image.get_rect()
        self.bg_image2 = pygame.transform.flip(pygame.image.load('images/city_bg.png'), True, False)
        self.rect2 = self.bg_image2.get_rect()

        self.bg_x1 = 0
        self.bg_y1 = 0

        self.bg_x2 = self.rect1.right
        self.bg_y2 = 0

    def update(self):
        self.bg_x1 -= self.scroll_speed
        self.bg_x2 -= self.scroll_speed
        if self.bg_x1 <= -3000:
            self.bg_x1 = 3000
        if self.bg_x2 <= -3000:
            self.bg_x2 = 3000

    def render(self):
        self.screen.blit(self.bg_image, (self.bg_x1, self.bg_y1))
        self.screen.blit(self.bg_image2, (self.bg_x2, self.bg_y2))


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x_coord):
        super().__init__()
        self.game = game
        self.settings = self.game.settings
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.scroll_speed = self.settings.scroll_speed

        self.image = pygame.image.load(os.path.join('images', 'platforms', 'grass_strip.png')).convert()
        self.rect = self.image.get_rect()
        self.rect.bottom = self.screen_rect.bottom
        self.rect.left = x_coord

    def update(self):
        self.rect.x -= self.scroll_speed

    def render(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))