import pygame
import pygame.font

class StatusBar:
    def __init__(self, game, bar_rect, color):
        self.game = game
        self.settings = self.game.settings
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()

        self.red = self.settings.red
        self.green = color

        self.health_bar = pygame.Rect(bar_rect)
        self.bg_health_bar = pygame.Rect(bar_rect)
        
    def update(self, change_factor):
        self.health_bar.width = change_factor

    def blitme(self):
        pygame.draw.rect(self.screen, self.red, self.bg_health_bar)
        pygame.draw.rect(self.screen, self.green, self.health_bar)


class ScreenMsg:
    def __init__(self, game, pic_path):
        self.game = game
        self.screen = self.game.screen
        self.screen_rect = self.screen.get_rect()

        self.image = pygame.image.load(pic_path).convert()

        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)



class Button:
    def __init__(self, game, msg):
        self.screen = game.screen
        self.screen_rect = self.screen.get_rect()

        self.width, self.height = 200, 50
        self.button_color = (255,25,25)
        self.text_color = (255,255,25)
        self.font = pygame.font.SysFont('Pokemon Hollow.ttf', 48)

        self.rect = pygame.Rect(0,0,self.width,self.height)
        self.rect.center = self.screen_rect.center

        self._prep_msg(msg)

    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)