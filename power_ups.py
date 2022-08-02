import pygame

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, game, pic_path):
        super().__init__()
        self.game = game
        self.settings = self.game.settings
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load(pic_path)
        self.rect = self.image.get_rect()

    # change factor is the variable that the powerup will increase
    def update(self, change_factor):
        self.rect.x -= self.settings.scroll_speed

    def blitme(self):
        self.screen.blit(self.image, self.rect)