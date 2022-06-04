import pygame
from settings import level_map, screen_height, tile_size, screen_width
from assets import *
from level_class import groups

# Classe Caracol
class Snail(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('Assets/sprites/teste/el caracol.png').convert_alpha() 
        self.image = pygame.transform.scale(self.image, (78,64))   
        self.rect = self.image.get_rect(topleft = position)  
        self.mask = pygame.mask.from_surface(self.image)
        self.speedx = -3

    def update(self, x_shift):    # Quando player chegar a uma parte do level, o level mexe para o lado (pygame é assim "press F")
        self.rect.x += x_shift + self.speedx
# ==============================================================================================================================================================================

# Classe Vespa
class Wasp(pygame.sprite.Sprite):
    def __init__(self):
        pass