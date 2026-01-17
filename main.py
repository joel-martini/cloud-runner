import pygame
from sys import exit
import random

class Cloud:
    def __init__(self, x, y, speed = 1, image="Assets/phcloud.png", index = 1, special=1):
        self.special = random.choices([0, 1, 2 ,3], weights=[0, 0.9, 0.05, 0.05])[0]
        if self.special ==1:
            image_path = "Assets/phcloud.png"
        elif self.special ==2:
            image_path = "Assets/phcloudgreen.png"
        elif self.special ==3:
            image_path = "Assets/phcloudred.png"
        self.surf = pygame.transform.scale(
            pygame.image.load(image_path).convert_alpha(),
            (128,16))
        self.rect = self.surf.get_rect(topleft=(x,y))
        self.speed = speed
        self.index = index
        self.image = image

    def update(self):
        if self.index == 1:
            self.rect.x += self.speed
            if self.rect.left > screen_width:
                self.rect.right = 0
        if self.index == 2:
            self.rect.x -= self.speed
            if self.rect.right < 0:
                self.rect.left = screen_width


    def draw(self, screen):
        screen.blit(self.surf, self.rect)



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
on_platform = False
#ground
ground_surf = pygame.image.load("Assets/groundph.png").convert_alpha()
ground_rect = ground_surf.get_rect(topleft=(0,screen_height- 150))

clouds = [
    Cloud(50, 350, index = 1), Cloud(50, 250, index = 2), Cloud(50, 150, index = 1), Cloud(50, 50, index =2),
    Cloud(250, 350, index = 1), Cloud(250, 250, index = 2), Cloud(250, 150, index = 1), Cloud(250, 50, index = 2),
    Cloud(450, 350, index = 1), Cloud(450, 250, index = 2), Cloud(450, 150, index = 1), Cloud( 450, 50, index = 2),
    Cloud(650, 350, index = 1), Cloud(650, 250, index = 2), Cloud(650, 150, index = 1), Cloud( 650, 50, index = 2),
]

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
    if keys[pygame.K_w] and on_platform:
        player_gravity = -15
    if keys[pygame.K_s]:
        if player_rect.bottom != ground_rect.top:
            player_gravity = 11




    for cloud in clouds:
        cloud.update()

    on_platform = False
    prev_bottom = player_rect.bottom
    prev_top = player_rect.top
    player_gravity += 1
    player_rect.y += player_gravity


    for cloud in clouds:
        if player_rect.colliderect(cloud.rect):

            # landing on top
            if player_gravity > 0 and prev_bottom <= cloud.rect.top:
                player_rect.bottom = cloud.rect.top
                player_gravity = 0
                on_platform = True

            # hitting underside
            elif player_gravity < 0 and prev_top >= cloud.rect.bottom:
                player_rect.top = cloud.rect.bottom
                player_gravity = 0

            # sides
            if (player_rect.right > cloud.rect.left and
                player_rect.left < cloud.rect.left and
                player_rect.bottom > cloud.rect.top + 5):
                player_rect.right = cloud.rect.left

            elif (player_rect.left < cloud.rect.right and
                  player_rect.right > cloud.rect.right and
                  player_rect.bottom > cloud.rect.top + 5):
                player_rect.left = cloud.rect.right

    if not on_platform and player_rect.bottom >= ground_rect.top:
        player_rect.bottom = ground_rect.top
        player_gravity = 0
        on_platform = True


    screen.fill((0,0,0))
    for cloud in clouds:
        cloud.draw(screen)
    screen.blit(player_surf, player_rect)
    screen.blit(ground_surf, ground_rect)
    pygame.display.flip()
    clock.tick(60)