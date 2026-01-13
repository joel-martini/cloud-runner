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
player_rect = player_surf.get_rect(midbottom=(screen_width//2, screen_height - 150))
player_speed = 5
player_gravity = 0
#ground
ground_surf = pygame.image.load("Assets/groundph.png").convert_alpha()
ground_rect = ground_surf.get_rect(topleft=(0,screen_height- 150))

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
    if keys[pygame.K_w]:
        if player_rect.bottom == ground_rect.top:
            player_gravity = -15
    if keys[pygame.K_s]:
        if player_rect.bottom != ground_rect.top:
            player_gravity = 11

    player_rect.y += player_gravity
    player_gravity = player_gravity + 1

    if player_rect.bottom >= ground_rect.top - 1:
        player_gravity = 0
        player_rect.bottom = ground_rect.top

    screen.fill((0,0,0))
    screen.blit(player_surf, player_rect)
    screen.blit(ground_surf, ground_rect)
    pygame.display.flip()
    clock.tick(60)