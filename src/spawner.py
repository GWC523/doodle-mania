import pygame
import random
from .enemy import Enemy

max_score = 0

class Spawner():
    global enemy_images
    total_enemies_spawned = 0
    time_elapsed = 0
    screen = 0
    time_between_spawns = 100
    concurrent_enemys = 0

    sound = 0

    def __init__(self, game_manager, screen):
        self.game_manager = game_manager
        self.screen = screen
        self.enemy_images= [
            pygame.image.load("Assets/Textures/enemy_1.png").convert_alpha(),
            pygame.image.load("Assets/Textures/enemy_2.png").convert_alpha(),
            pygame.image.load("Assets/Textures/enemy_3.png").convert_alpha(),
        ]
         # Initial and minimum time between spawns in seconds
        self.initial_time_between_spawns = 2
        self.min_time_between_spawns = 0.2  # The fastest spawn rate you want to allow
        self.time_between_spawns = self.initial_time_between_spawns

        # The amount of time in seconds to wait before increasing the spawn rate
        self.spawn_rate_increase_interval = 3
        self.time_since_last_increase = 0


    def check_for_player(self, player):
        global score_int
        for entity in self.game_manager.entities_alive:
            if pygame.sprite.collide_mask(player.player_sprite, entity.position):
                if(entity.tag == "enemy"):
                    self.game_manager.lives -= 1
                    player.update_alpha()
                    self.game_manager.entities_alive.remove(entity)
                    if self.game_manager.lives <= 0:
                        self.game_manager.game_state = 0
                    self.game_manager.update_max_score(self.game_manager.score)
        
    def set_time_between_spawns(self, time_between_spawns):
        self.time_between_spawns = time_between_spawns
    
    def draw_enemies(self, dt):
        for i in range(len(self.game_manager.entities_alive)):
            try:
                self.game_manager.entities_alive[i].draw(self.screen)
                self.game_manager.entities_alive[i].move(dt)
                self.game_manager.entities_alive[i].collisions(self.game_manager.entities_alive)
            except:
                pass

    def timer(self, dt):
        self.time_elapsed += dt
        self.time_since_last_increase += dt

        # Check if it's time to increase the spawn rate
        if self.time_since_last_increase > self.spawn_rate_increase_interval:
            self.time_since_last_increase = 0 

            # Increase the spawn rate by reducing the time between spawns
            self.time_between_spawns = max(
                self.min_time_between_spawns, 
                self.time_between_spawns * 0.9 
            )
    
    def spawner(self):
        if(self.time_elapsed >= self.time_between_spawns):
            selected_image = random.choice(self.enemy_images)
            entity = Enemy(selected_image)
            self.concurrent_enemys += 1
            self.game_manager.entities_alive.append(entity)

            self.time_elapsed = 0