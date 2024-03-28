import pygame

class Player():
    global game_state
    #Transform
    position = pygame.Vector2()
    scale = pygame.Vector2()

    #Physics
    velocity_y = 0
    gravity_scale = 3000
    speed = 400
    is_grounded = False

    #Graphics
    player_sprite = 0
    rotation = 0
    rot_speed = 400

    scale_speed = 3

    player_collider = 0


    def __init__(self, game_manager, desired_scale_x, desired_scale_y, Width, Height):
        self.game_manager = game_manager
        self.scale.x = desired_scale_x
        self.scale.y = desired_scale_y

        self.scalar = 50

        self.player_sprite = pygame.sprite.Sprite()
        self.player_sprite.image = pygame.image.load("Assets/Textures/Ducky.png").convert_alpha()
        self.player_sprite.image = pygame.transform.scale(self.player_sprite.image, (int(self.scale.x), int(self.scale.y)))
        self.player_sprite.mask = pygame.mask.from_surface(self.player_sprite.image)

        self.position.x = Width / 2
        self.position.y = Height * 3 / 4 + 10

        self.player_sprite.rect = self.player_sprite.image.get_rect()

        self.scalar = self.scale.x


    def move(self, keys, dt):
        global score_int
        global score
        global max_score

        if(keys[0]):
            self.position.x -= 0.01 * dt * self.speed
        if(keys[1]):
            self.position.x += 0.01 * dt * self.speed

        self.velocity_y += 0.00001 * dt * self.gravity_scale

        self.position.y += self.velocity_y * dt

        self.player_sprite.rect.topleft = self.position.x, self.position.y
        self.player_sprite.rect.center = (self.position.x, self.position.y)

    def update_alpha(self):
        self.game_manager.alpha = self.game_manager.lives * 55

    def draw(self, screen, colliders):
        img_copy = pygame.transform.scale(self.player_sprite.image, (int(self.scalar), int(self.scalar)))
        img_copy.fill((255, 255, 255, self.game_manager.alpha), None, pygame.BLEND_RGBA_MULT)
        self.collisions(colliders, img_copy.get_height())
        screen.blit(img_copy, (self.position.x - int(img_copy.get_width() / 2), self.position.y - int(img_copy.get_height() / 2)))
        self.player_sprite.rect.center = (self.position.x, self.position.y)
        
    def collisions(self, colliders, scale):
        #Top of box
        self.is_grounded = False
        for i in range(len(colliders)):
            if(self.position.y - int(scale / 2) >= colliders[i].top - scale and colliders[i].typeof == "environment"):
                self.is_grounded = True
                self.position.y = colliders[i].top - int(scale / 2) + 13
                self.velocity_y  = 0
            if(self.position.x + int(self.player_sprite.image.get_width() / 2) >= 720):
                self.position.x = 720 - int(self.player_sprite.image.get_width() / 2)
            if(self.position.x - int(self.player_sprite.image.get_width() / 2) <= 0):
                self.position.x = 0 + int(self.player_sprite.image.get_width() / 2)