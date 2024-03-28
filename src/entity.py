import pygame

class Entity():
    tag = "Default"
    bottom = 0
    sound = 0

    right = 0
    left = 0

    def move(self, dt):
        self.position.rect.y += dt * self.speed
        self.bottom = self.position.rect.bottom
        self.right = self.position.rect.right
        self.left = self.position.rect.left

    def collisions(self, enemies):
        if(self.position.rect.y > 390):
            enemies.remove(self)
            enemies = enemies[:-1]
            self.sound.play()

    def initialiser(self, color, sfx_path):
        self.sound = pygame.mixer.Sound(sfx_path)

    def draw(self, screen):
        screen.blit(self.position.image, self.position.rect)