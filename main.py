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
player_rect = player_surf.get_rect(center=(screen_width//2, screen_height - 150))
player_speed = 5

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if player_rect.x > 0:
            player_rect.x += player_speed * -1
    if keys[pygame.K_d]:
        if player_rect.x < screen_width - player_rect.width:
            player_rect.x += player_speed

    screen.fill((0,0,0))
    screen.blit(player_surf, player_rect)
    pygame.display.flip()
    clock.tick(60)