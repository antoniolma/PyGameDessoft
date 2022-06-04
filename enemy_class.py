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
    
    def snail_moviment(self):
    
        collision_snail_inv = pygame.sprite.groupcollide(groups['all_snails'], groups['invisible_tiles'], False, False)
        collision_snail_tile = pygame.sprite.groupcollide(groups['all_snails'], groups['all_tiles'], False, False)

        for snail, tiles in collision_snail_inv.items():
            bloco = tiles[0]

            # Caracol indo para direita
            if bloco.rect.right > snail.rect.right > bloco.rect.left:
                snail.rect.right = bloco.rect.left
                snail.speedx = -snail.speedx
                self.image = pygame.image.load('Assets/sprites/teste/el caracol.png').convert_alpha() #Quando colide, vira para esquerda
                self.image = pygame.transform.scale(self.image, (78,64))

            # Caracol indo para esquerda
            elif bloco.rect.left < snail.rect.left < bloco.rect.right:
                snail.rect.left = bloco.rect.right
                snail.speedx = -snail.speedx
                self.image = pygame.image.load('Assets/sprites/teste/caracol_d.png').convert_alpha() #Quando colide, vira para direita
                self.image = pygame.transform.scale(self.image, (78,64))

        for snail, tiles in collision_snail_tile.items():
            bloco = tiles[0]

            # Caracol indo para direita
            if bloco.rect.right > snail.rect.right > bloco.rect.left:
                snail.rect.right = bloco.rect.left
                snail.speedx = -snail.speedx
                self.image = pygame.image.load('Assets/sprites/teste/el caracol.png').convert_alpha() #Quando colide, vira para esquerda
                self.image = pygame.transform.scale(self.image, (78,64))

            # Caracol indo para esquerda
            elif bloco.rect.left < snail.rect.left < bloco.rect.right:
                snail.rect.left = bloco.rect.right
                snail.speedx = -snail.speedx
                self.image = pygame.image.load('Assets/sprites/teste/caracol_d.png').convert_alpha() #Quando colide, vira para direita
                self.image = pygame.transform.scale(self.image, (78,64))

                
    def update(self, x_shift):    # Quando player chegar a uma parte do level, o level mexe para o lado (pygame é assim "press F")
        self.rect.x += x_shift + self.speedx
        self.snail_moviment()
# ==============================================================================================================================================================================

# Classe Vespa
class Wasp(pygame.sprite.Sprite):
    def __init__(self):
        pass