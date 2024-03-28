import pygame
import random
from .entity import Entity


class Enemy(Entity):
    def __init__(self, image):
        self.speed = random.randrange(2, 5)
        self.enemy_sprite = pygame.sprite.Sprite()
        self.enemy_sprite.image = image
        self.enemy_sprite.image = pygame.transform.scale(self.enemy_sprite.image, (60, 60))
        self.enemy_sprite.rect = self.enemy_sprite.image.get_rect()
        self.enemy_sprite.mask = pygame.mask.from_surface(self.enemy_sprite.image)

        self.position = self.enemy_sprite
        self.position.rect.x = random.randrange(0, 720)
        self.position.rect.y = 0

        self.initialiser((102, 107, 102), "Assets/Audio/RockHit.wav")

        self.tag = "enemy"