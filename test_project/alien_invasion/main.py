import sys
import pygame

from settings import Settings


class Ship():

    def __init__(self,screen):

        self.screen = screen

        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rec()
        self.screen.rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

    def blitme(self):
        self.screen.blit(self.image,self.rect)


def run_game():
    pygame.init()

    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    bg_color= (230,230,230)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.fill(ai_settings.bg_color)

        pygame.display.flip()

run_game()
