import pygame
import os

class Platform(pygame.sprite.Sprite):
    def __init__(self, img, order, game): # 'order' is the order the platform is in
# like if there are 2 platforms in this rotation, the first 'order' arg will be 1, 2nd is 2
        super().__init__()
        self.game = game
        self.settings = self.game.settings
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load(os.path.join('images', img))
        self.rect = self.image.get_rect()

    def update(self):
        if self.rect.right >= self.screen_rect.left:
            self.rect.x -= self.settings.scroll_speed
        if self.rect.right <= 0:
            self.kill()

    def blitme(self):
        self.screen.blit(self.image, self.rect)