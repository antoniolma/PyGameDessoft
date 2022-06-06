import pygame
from settings import level_map, screen_height, tile_size, screen_width
from assets import *

# Classe do Carlos, o Macaco
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        [self.player_w, self.player_h] = [ tile_size, tile_size ]   # player size

        # Sprite do player
        self.desenho = assets[PLAYER].convert_alpha()  #player img 
        self.image = pygame.transform.scale(self.desenho, (self.player_w, self.player_h))   # Rescale the player
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = self.player_w
        self.rect.centery = self.player_h / 2
        self.groups = groups
        self.lvl_section = 1
        self.centerx = self.player_w/2
        self.was_hit = False

        # Score do player
        self.score = 0

        # Mercando de quanto em quanto tempo é possível atirar
        self.last_shot = pygame.time.get_ticks()
        self.last_hit = 0
        
        self.shoot_ticks = 500
        self.dmg_ticks = 100
        
        # Movimento
        self.can_move = True
        self.direction = pygame.math.Vector2(0,0)  # Cria um Vetor2 (2 dimensões) (lista de valores x e y)
        self.speedx = 4
        self.gravity = 0.8
        self.jump_speed = -16
        self.can_jump = True
        self.lado_atirar = self.rect.right
        self.last_dx = 0

        # Munição disponível (que aparece para o player)
        self.banana_storage = pygame.sprite.Group()
        x = 30

        for i in range(3):
            x += 30
            balas_restantes = Munition(x, 10)
            self.banana_storage.add(balas_restantes)
            self.groups["all_sprites"].add(balas_restantes)

        # Vida 
        self.hp = 0
        self.live = pygame.sprite.Group()
        x = 35

        for i in range(3):
            x += 30
            vidas_restantes = Heart(x, 50)
            self.groups["all_sprites"].add(vidas_restantes)
            self.live.add(vidas_restantes)
            self.hp += 1


    # Pega as teclas pressionadas relacionadas ao player
    def get_input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            # Movimento pros lados
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.lado_atirar = self.rect.right
                if self.was_hit == False:
                    self.desenho = pygame.image.load('Assets/sprites/teste/el mamaco parado.png').convert_alpha()
                    self.image = pygame.transform.scale(self.desenho, (self.player_w, self.player_h))
                elif self.was_hit:
                    self.desenho = pygame.image.load('Assets/sprites/teste/monkey_righthit.png').convert_alpha()
                    self.image = pygame.transform.scale(self.desenho, (self.player_w, self.player_h))
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.lado_atirar = self.rect.left
                if self.was_hit == False:
                    self.desenho = pygame.image.load('Assets/sprites/teste/mamaco_virado.png').convert_alpha()
                    self.image = pygame.transform.scale(self.desenho, (self.player_w, self.player_h))
                elif self.was_hit:
                    self.desenho = pygame.image.load('Assets/sprites/teste/monkey_lefthit.png').convert_alpha()
                    self.image = pygame.transform.scale(self.desenho, (self.player_w, self.player_h))
            else:
                self.direction.x = 0
            
        # Movimento pulo
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.jump()

        # Atirar
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        # Não permite personagem sair da tela
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.left < 0:
            self.rect.left = 0 

        # Não permite que o personagem pule para além da tela
        if self.rect.top < 0:
            self.rect.top = 0
        
        # if keys[pygame.K_RCTRL]:
        #     self.draw()

    # Gravidade sobre o player
    def apply_gravity(self):
        if self.direction.y >= 32:
            self.direction.y = 32
        self.direction.y += self.gravity  # Todo frame desce 0.8 em Y
        self.rect.y += self.direction.y   # O retângulo do player se move

    def jump(self):
        if self.can_jump:
            self.direction.y = self.jump_speed
            self.can_jump = False

    def shoot(self):
        if len(self.banana_storage) > 0:
            # Verifica se pode atirar
            now = pygame.time.get_ticks()
            # Verifica quantos ticks se passaram desde o último tiro.
            elapsed_ticks = now - self.last_shot

            # Se já pode atirar novamente...
            if elapsed_ticks > self.shoot_ticks:
                self.banana_storage.sprites()[-1].kill()
                # Marca o tick da nova imagem.
                self.last_shot = now

                banana_speed = 10
                if self.last_dx < 0:
                    banana_speed = -10
                
                # Criando nova banana
                bananinha = Banana(self.rect.centery, self.lado_atirar, banana_speed)
                self.groups['all_sprites'].add(bananinha)
                self.groups['all_bananas'].add(bananinha)
    
    # def gethit_jump(self):
    #     if self.direction.y != 0:
    #         self.direction.y = -8
    #     self.can_jump = True

    #     if self.last_dx > 0:
    #         self.direction.x = -0.5
    #     elif self.last_dx < 0:
    #         self.direction.x = 0.5
    
    # Atualiza o player
    def update(self):
        self.get_input()

        if self.was_hit:
            now = pygame.time.get_ticks()
            elapsed_ticks = now - self.last_hit
            if elapsed_ticks > self.dmg_ticks:
                self.was_hit = False

        if self.direction.x != 0:
            self.last_dx = self.direction.x

# ==============================================================================================================================================================================

# Classe do tiro
class Banana(pygame.sprite.Sprite):
    def __init__(self, centery, ladoplayer, banana_speed):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('Assets/sprites/teste/banana munição.png').convert_alpha()  #player img 
        self.image = pygame.transform.scale(self.image, (16, 16))   # Rescale the player
        self.rect = self.image.get_rect() 
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.centery = centery + 15
        self.rect.left = ladoplayer
        if banana_speed < 0:
            self.rect.right = ladoplayer
        self.speedx = banana_speed

    def update(self):
        # A bala só se move no eixo x
        self.rect.x += self.speedx
        if self.rect.x < - 50 or self.rect.x > screen_width + 50:
            self.kill()

# ==============================================================================================================================================================================

# Classe da Munição do Macaco      
class Munition(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Assets/sprites/teste/municao.png').convert_alpha() 
        self.image = pygame.transform.scale(self.image, (32,32))   
        self.rect = self.image.get_rect() 

        self.rect.top = y
        self.rect.left = x

# ==============================================================================================================================================================================

# Classe dos sprites de vida 
class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Assets/sprites/teste/live.png').convert_alpha() 
        self.image = pygame.transform.scale(self.image, (16,16))   
        self.rect = self.image.get_rect() 

        self.rect.top = y
        self.rect.left = x
