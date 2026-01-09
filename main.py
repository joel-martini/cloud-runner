import pygame
from sys import exit


pygame.init()

#variables
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cloud Runner")
clock = pygame.time.Clock()
#player
player_surf = pygame.transform.scale(pygame.image.load("Assets/phplayer.png").convert_alpha(), (32,32))
player_rect = player_surf.get_rect(center=(screen_width//2, screen_height//2))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    screen.blit(player_surf, player_rect)
    pygame.display.flip()
    clock.tick(60)