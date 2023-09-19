import pygame
from assets import *
from level_class import groups

# Classe Caracol
class Snail(pygame.sprite.Sprite):
    # Inicialização do Caracol, inimigo móvel do jogo
    def __init__(self, position, size):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('Assets/sprites/teste/el caracol.png').convert_alpha() 
        self.image = pygame.transform.scale(self.image, (78,64))   
        self.rect = self.image.get_rect(topleft = position)  
        
        self.speedx = -2
    
    def snailImage(self, direction):
        if direction == "left":
            self.image = pygame.image.load('Assets/sprites/teste/el caracol.png').convert_alpha() #Quando colide, vira para esquerda
            self.image = pygame.transform.scale(self.image, (78,64))
            self.mask = pygame.mask.from_surface(self.image)

        elif direction == "right":
            self.image = pygame.image.load('Assets/sprites/teste/caracol_virado.png').convert_alpha() #Quando colide, vira para direita
            self.image = pygame.transform.scale(self.image, (78,64))
            self.mask = pygame.mask.from_surface(self.image)

    def snailCollision(self):

        collision_snail_inv = pygame.sprite.groupcollide(groups['all_snails'], groups['invisible_tiles'], False, False)
        collision_snail_tile = pygame.sprite.groupcollide(groups['all_snails'], groups['all_tiles'], False, False)

        for snail, tiles in collision_snail_inv.items():
            bloco = tiles[0]

            # Caracol indo para direita
            if bloco.rect.right > snail.rect.right > bloco.rect.left:
                direction = "right"
                self.snailImage(direction)
                snail.rect.right = bloco.rect.left
                snail.speedx = -snail.speedx
                
            # Caracol indo para esquerda
            elif bloco.rect.left < snail.rect.left < bloco.rect.right:
                direction = "left"
                self.snailImage(direction)
                snail.rect.left = bloco.rect.right
                snail.speedx = -snail.speedx
                
        for snail, tiles in collision_snail_tile.items():
            bloco = tiles[0]

            # Caracol indo para direita
            if bloco.rect.right > snail.rect.right > bloco.rect.left:
                direction = "right"
                self.snailImage(direction)
                snail.rect.right = bloco.rect.left
                snail.speedx = -snail.speedx

            # Caracol indo para esquerda
            elif bloco.rect.left < snail.rect.left < bloco.rect.right:
                direction = "left"
                self.snailImage(direction)
                snail.rect.left = bloco.rect.right
                snail.speedx = -snail.speedx

    def snailMovement(self, x_shift):
        '''
        Programa o movimento do caracol: ele se move até bater em um tile (geralmente, o invisível)
        quando isso ocorre, a velocidade (direção) inverte
        '''
        self.rect.x += x_shift + self.speedx

    def update(self, x_shift):    # Quando player chegar a uma parte do level, o level mexe para o lado (pygame é assim "press F")
        self.snailMovement(x_shift)
        self.snailCollision()
        

# ==============================================================================================================================================================================

# Classe spikes
class Espinho(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()

        self.image = pygame.image.load('Assets/sprites/teste/espinhos.png')  
        self.image = pygame.transform.scale(self.image, (size,size))
        self.rect = self.image.get_rect(topleft = position)
    
    def update(self, x_shift):    # Quando player chegar a uma parte do level, o level mexe para o lado
        self.rect.x += x_shift