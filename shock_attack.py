import pygame
from pygame.sprite import Sprite

class ShockAttack(Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen = self.game.screen
        self.settings = self.game.settings
        self.screen_rect = self.game.screen_rect

        # this is the code for the new shock
        self.image_names = [f"shock_{x}.png" for x in range(1,10)]
        self.r_imgs = [pygame.image.load(f"images/shock/{x}") for x in self.image_names]
        self.l_imgs = [pygame.transform.flip(img, True, False) for img in self.r_imgs]
        if self.game.pikachu.facing == 'R':
            self.images = self.r_imgs
        else:
            self.images = self.l_imgs
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

    def update(self):
        if self.game.pikachu.facing == 'R':
            self.image = self.r_imgs[self.index]
            self.rect = self.image.get_rect()
            self.rect.midleft = self.game.pikachu.rect.midright
        else:
            self.image = self.l_imgs[self.index]
            self.rect = self.image.get_rect()
            self.rect.midright = self.game.pikachu.rect.midleft

    def blitme(self):
        self.screen.blit(self.image, self.rect)