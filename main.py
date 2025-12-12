import pygame
from sys import exit

pygame.init()

# classes
class Cloud:
    def __init__(self, x, y, speed=0, image="Assets/cloud1.png"):
        self.surf = pygame.image.load(image).convert_alpha()
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.surf, self.rect)


# Setup
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# player
player_surf = pygame.image.load("Assets/playertest1.png").convert_alpha()
player_rect = player_surf.get_rect(center=(88, 300)) #screen_width / 2         screen_height - 166
player_speed = 5
player_gravity = 0
jump_height = 15
can_jump = False

# ground
ground_surf = pygame.image.load("Assets/ground.png").convert_alpha()
ground_rect = ground_surf.get_rect(topleft=(0, (screen_height - 150)))

# items
item_surf = pygame.image.load("Assets/item1.png").convert_alpha()
item_rect = item_surf.get_rect(center=(552, 75))
item_picked_up = False

#death
spike_surf = pygame.transform.scale(pygame.image.load("Assets/gameover.png").convert_alpha(), (800, 16))
spike_rect = spike_surf.get_rect(bottomleft=(0, 450))

# clouds
cloudmovex = 0
cloudmoveindex = 1
room = 5
deaths = 0
print("room " + str(room))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_rect.x += player_speed

    if room == 1:
        clouds = [
            Cloud(0, ground_rect.y - 75),  # 1
            Cloud(300, 350),  # 2
            Cloud(cloudmovex + 450, 250),  # move
            Cloud(180, 220),  # 4
            Cloud(450, 120),  # 5
        ]
    elif room == 2:
        clouds = [
            Cloud(0, ground_rect.y - 75),
            Cloud(0, 300),
            Cloud(330, 300),
            Cloud(330, 200)
        ]
    elif room == 3:
        item_rect.center = (130,130)
        clouds = [
            Cloud(70, ground_rect.y - 75),
            Cloud(400, ground_rect.y - 75),
            Cloud(550, 280),
            Cloud(550, 200),
            Cloud(240, 200),
            Cloud(420, 100)
        ]
    elif room == 4:
        item_rect.center = (400,170)
        clouds = [
            Cloud(0, ground_rect.y - 75),
            Cloud(300, ground_rect.y - 75),
            Cloud(550, 300),
            Cloud(550, 200),
            Cloud(310,100),
            Cloud(471, 100,0,"Assets/cloud2.png"),
            Cloud(50, 200),
            Cloud(cloudmovex + 177, 250)
        ]
    elif room == 5:
        item_rect.center = (750, ground_rect.y - 50)
        clouds = [
            Cloud(20, ground_rect.y - 75),
            Cloud(270, 300),
            Cloud(270, 210),
            Cloud(550, 100),
            Cloud(250, 120)
        ]


    # horizontal boundaries
    player_rect.x = max(0, min(player_rect.x, 784))

    # gravity
    prev_bottom = player_rect.bottom
    player_gravity += 1
    player_rect.y += player_gravity
    on_platform = False

    # cloud collisions
    for cloud in clouds:
        if player_rect.colliderect(cloud.rect):

            # landing on top
            if player_gravity > 0 and prev_bottom <= cloud.rect.top and player_rect.bottom >= cloud.rect.top:
                player_rect.bottom = cloud.rect.top
                player_gravity = 0
                on_platform = True

            # hitting underside
            elif player_gravity < 0 and player_rect.top <= cloud.rect.bottom and player_rect.centery > cloud.rect.bottom:
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

    if player_rect.bottom >= ground_rect.top:
        player_rect.bottom = ground_rect.top
        player_gravity = 0
        on_platform = True

    # ground collision
    if on_platform:
        can_jump = True
    else:
        can_jump = False

    # jumping
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and on_platform:
        player_gravity = -jump_height

    # soft drop
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_rect.bottom <= screen_height - 150:
        player_gravity = jump_height * 0.6

    if player_rect.colliderect(item_rect):
        if item_picked_up == False:
            room += 1
            print("room "+ str(room))
            player_rect.center = (88, 367)

    # death
    if player_rect.colliderect(spike_rect):
        deaths += 1
        print("death " + str(deaths))
        player_rect.center = (88, 367)

    if cloudmoveindex == 1:
        cloudmovex += 1
    elif cloudmoveindex == 2:
        cloudmovex -= 1

    if cloudmovex >= 50:
        cloudmoveindex = 2
    elif cloudmovex <= 0:
        cloudmoveindex = 1

    # drawing
    screen.fill((0, 0, 0))
    screen.blit(ground_surf, ground_rect)
    screen.blit(player_surf, player_rect)
    if item_picked_up == False:
        screen.blit(item_surf, item_rect)
    screen.blit(spike_surf, spike_rect)

    for cloud in clouds:
        cloud.update()
        cloud.draw(screen)

    pygame.display.update()
    clock.tick(60)

