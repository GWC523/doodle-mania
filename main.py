import pygame
from pygame.locals import *
from src.player import Player
from src.spawner import Spawner
from src.gameManager import GameManager
from src.boxCollider import Box_Collider
import time

class Main():
    previous_frame_time = 0
    dt = 0
    elapsed_time = 0
    time_between_spawns = 100
    
    def calculate_deltatime(self):
        self.dt = time.time() - self.previous_frame_time
        self.dt *= 60
        self.previous_frame_time = time.time()

    def difficulty(self):
        self.elapsed_time += self.dt
        if(self.elapsed_time > 1000):
            self.time_between_spawns /= 1.45
            self.elapsed_time = 0

    def handle_inputs(self, keys, event):
        if(event.type == pygame.KEYDOWN):
            if(event.key == K_a):
                keys[0] = True
            if(event.key == K_d):
                keys[1] = True
        if(event.type == pygame.KEYUP):
            if(event.key == K_a):
                keys[0] = False
            if(event.key == K_d):
                keys[1] = False
    
    def setup_pygame(self, title, width, height):
        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        favicon = pygame.image.load("Assets/Textures/Ducky.png").convert_alpha()
        pygame.display.set_icon(favicon)
        pygame.init()
        return screen

    def update_score(self, screen, text):
        global score_int
        self.game_manager.score += self.dt / 100
        score_int = int(self.game_manager.score)
        score_text = text.render("SCORE: " + str(score_int),True,(0,0,0))
        screen.blit(score_text, (10, 10))

    def draw_lives(self, screen, player, text):
        lives_text = text.render("Lives: " + str(self.game_manager.lives), True, (0, 0, 0))
        screen.blit(lives_text, (10, 55))

    def draw_colliders(self, colliders, screen, color, width, height):
        for i in range(len(colliders)):
            colliders[i].draw(screen, color, width, height)

    def reset_state(self):
        self.previous_frame_time = 0
        self.dt = 0
        self.elapsed_time = 0
        self.time_between_spawns = 100
        self.score_int = 0
        
    def game(self, screen, font, WIDTH, HEIGHT):
        WHITE = (255, 255, 255)

        self.previous_frame_time = time.time()

        keys = [False, False, False]

        player = Player(self.game_manager, 80, 80, WIDTH, HEIGHT)

        colliders = []

        #Background sprite
        foreground = pygame.sprite.Sprite()
        foreground.image = pygame.image.load("Assets/Textures/Foreground.png").convert_alpha()
        foreground.rect = foreground.image.get_rect()
        foreground.rect.topleft = 0, HEIGHT - 480
        foreground.image = pygame.transform.scale(foreground.image, (720, 480))
        foreground_collider = Box_Collider(WIDTH / 2, HEIGHT - 20, 720, 120, "environment")

        colliders.append(foreground_collider)

        spawner = Spawner(self.game_manager, screen)

        time_elapsed = 0

        while(self.game_manager.game_state == 1):
            screen.fill(WHITE)
            for event in pygame.event.get():
                if(event.type == pygame.QUIT):
                    self.game_manager.game_state = 2
                self.handle_inputs(keys, event)
            self.difficulty()
            self.calculate_deltatime()

            screen.blit(foreground.image, foreground.rect)
            
            time_elapsed += self.dt
            
            if(time_elapsed > 10):
                time_elapsed = 0

            player.move(keys, self.dt)
            player.draw(screen, colliders)

            spawner.spawner()
            spawner.set_time_between_spawns(self.time_between_spawns)
            spawner.timer(self.dt)
            spawner.draw_enemies(self.dt)
            spawner.check_for_player(player)


            self.update_score(screen, font)
            self.draw_lives(screen, player, font)

            pygame.display.update()

    def menu(self, screen, font, WIDTH, HEIGHT):
        # Load background image
        background_image = pygame.image.load("Assets/Textures/Thumbnail.png").convert()

        sound = pygame.mixer.Sound("Assets/Audio/Start_bg.mp3")
        score_text = font.render("HIGH SCORE: " + str(int(self.game_manager.max_score)), True, (0, 0, 0, 100))

        while self.game_manager.game_state == 0:
            screen.blit(background_image, (0, 0))
            screen.blit(score_text, (WIDTH/2 - score_text.get_width() / 2, HEIGHT/2 - score_text.get_height() / 2 + 38))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sound.stop()
                    self.game_manager.game_state = 2
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_SPACE: 
                        self.game_manager.game_state = 1
                        pygame.mixer.quit() 
                        pygame.mixer.init()
                        sound.play(-1)

            pygame.display.update()
                       
    def __init__(self):
        self.game_manager = GameManager()
        
        while self.game_manager.game_state != 2:
            WIDTH, HEIGHT = 720, 480

            screen = self.setup_pygame("Doodle Mania I", WIDTH, HEIGHT)
            font = pygame.font.Font("Assets/Fonts/more-sugar.regular.ttf", 32)

            if(self.game_manager.game_state == 0):
                self.menu(screen, font, WIDTH, HEIGHT)
            if(self.game_manager.game_state == 1):
                self.previous_frame_time = time.time()
                self.game(screen, font, WIDTH, HEIGHT)
            
            sound = pygame.mixer.Sound("Assets/Audio/Scribble.mp3")
            sound.play()
            self.reset_state()
            self.game_manager.reset_game()
            self.game_manager.entities_alive.clear()
            self.game_manager.entities_alive = []
            
game = Main()