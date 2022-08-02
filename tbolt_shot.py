import pygame

class TboltShot(pygame.sprite.Sprite):
    def __init__(self, game, x_rect):
        super().__init__()
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.screen_rect = self.game.screen_rect
        
        # the x coord when tbolt is shot - itll go horizontally across screen
        self.path = x_rect

        self.image_names = ['tbolt_shot_'+str(x)+'.png' for x in range(1,11)]
        self.r_imgs = [pygame.image.load(f'images/tbolt_shot/{x}') for x in self.image_names]
        self.l_imgs = [pygame.transform.flip(img, True, False) for img in self.r_imgs]

        self.index = 0
        # self.image = self.images[self.index]
        # self.rect = self.image.get_rect()

        if self.game.pikachu.facing == 'R':
            self.images = self.r_imgs
            # set direction that bolt will fire
            self.direction = 'R'
        else:
            self.images = self.l_imgs
            self.direction = 'L'
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()

        if self.game.pikachu.facing == 'R':
            self.rect.midleft = self.game.pikachu.rect.midright
            self.rect.x + 10
        else:
            self.rect.midright = self.game.pikachu.rect.midleft
            self.rect.x - 10

        # boolean - if it's True - then kill the tbolt
        self.disappear = False

    def update(self):

        self.image = self.images[self.index]
        if self.game.tbolt_move:
            if self.direction == 'R':
                self.rect.x += self.settings.tbolt_shot_speed
            else:
                self.rect.x -= self.settings.tbolt_shot_speed
        elif not self.game.tbolt_move:
            self.rect.x -= self.settings.scroll_speed
            if self.game.pikachu.facing == 'R':
                self.rect.midleft = self.game.pikachu.rect.midright
            else:
                self.rect.midright = self.game.pikachu.rect.midleft
        self._disappear()

    def _disappear(self):
        if self.disappear or (self.rect.x > 800 or self.rect.x < 0):
            self.kill()

    def blitme(self):
        self.screen.blit(self.image, self.rect)

        

