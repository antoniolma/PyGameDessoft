import pygame
from settings import level_map, screen_height, tile_size, screen_width
from assets import *

groups = {}  # Inicializa diionário que conterá os grupos de sprites
all_bananas = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_snails = pygame.sprite.Group()
all_tiles = pygame.sprite.Group()
groups['all_sprites'] = all_sprites
groups['all_bananas'] = all_bananas
groups['all_snails'] = all_snails
groups['all_tiles'] = all_tiles

# Classe do Carlos, o Macaco
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        [self.player_w, self.player_h] = [ tile_size, tile_size ]   # player size

        # Player Status
        self.hp = 3          # Vida do personagem
        
        # Sprite do player
        self.image = assets[PLAYER].convert_alpha()  #player img 
        self.image = pygame.transform.scale(self.image, (self.player_w, self.player_h))   # Rescale the player
        self.rect = self.image.get_rect(topleft = pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.left = self.player_w
        self.rect.centery = self.player_h / 2
        self.groups = groups
        self.lvl_section = 1
        self.centerx = self.player_w/2

        # Mercando de quanto em quanto tempo é possível atirar
        self.last_shot = pygame.time.get_ticks()
        self.last_hit = pygame.time.get_ticks()
        self.shoot_ticks = 500
        
        # Movimento
        self.can_move = True
        self.direction = pygame.math.Vector2(0,0)  # Cria um Vetor2 (2 dimensões) (lista de valores x e y)
        self.speedx = 4
        self.gravity = 0.8
        self.jump_speed = -18
        self.can_jump = True

        # Munição disponível (que aparece para o player)
        self.banana_storage = pygame.sprite.Group()
        x = pos[0]

        for i in range(3):
            x += 30
            balas_restantes = Munition(x, 10)
            self.banana_storage.add(balas_restantes)
            self.groups["all_sprites"].add(balas_restantes)

        # Vida 
        self.live = pygame.sprite.Group()
        x = pos[0]

        for i in range(3):
            x += 30
            vidas_restantes = Heart(x, 40)
            self.groups["all_sprites"].add(vidas_restantes)


    # Pega as teclas pressionadas relacionadas ao player
    def get_input(self):
        keys = pygame.key.get_pressed()

        if self.can_move:
            # Movimento pros lados
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.image = pygame.image.load('Assets/sprites/teste/el mamaco parado.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.player_w, self.player_h))
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.image = pygame.image.load('Assets/sprites/teste/mamaco_virado.png').convert_alpha()
                self.image = pygame.transform.scale(self.image, (self.player_w, self.player_h))
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
                # Criando nova banana
                bananinha = Banana(self.rect.centery, self.rect.right)
                self.groups['all_sprites'].add(bananinha)
                self.groups['all_bananas'].add(bananinha)
        
    def was_hit(self):
         # Consequências ao player
        self.live.sprites()[-1].kill()
        print(self.live)
        self.jump_cd = False
        self.can_move = False

        # ----- Reação a Hit
        self.jump()
        # Pulinho pra esquerda
        if self.direction.x > 0:
            self.direction.x = -10
        # Pulinho pra direita
        elif self.direction.x < 0: 
            self.direction.x = 10

    # Atualiza o player
    def update(self):
        self.get_input()


# Classe Inimigo: Caracol
class Snail(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('Assets/sprites/teste/el caracol.png').convert_alpha() 
        self.image = pygame.transform.scale(self.image, (78,64))   
        self.rect = self.image.get_rect(topleft = position)  
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, x_shift):    # Quando player chegar a uma parte do level, o level mexe para o lado (pygame é assim "press F")
        self.rect.x += x_shift

# Classe do tiro
class Banana(pygame.sprite.Sprite):
    def __init__(self, centery, rightplayer):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('Assets/sprites/teste/banana munição.png').convert_alpha()  #player img 
        self.image = pygame.transform.scale(self.image, (16, 16))   # Rescale the player
        self.rect = self.image.get_rect() 
        self.mask = pygame.mask.from_surface(self.image)

        self.rect.centery = centery + 15
        self.rect.left = rightplayer - 35
        self.speedx = 10

    def update(self):
        # A bala só se move no eixo x
        self.rect.x += self.speedx
        if self.rect.x < - 50 or self.rect.x > screen_width + 50:
            self.kill()


# Classe dos sprites que indicam ao jogador quantas bananas eles tem disponíveis         
class Munition(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Assets/sprites/teste/municao.png').convert_alpha() 
        self.image = pygame.transform.scale(self.image, (32,32))   
        self.rect = self.image.get_rect() 

        self.rect.top = y
        self.rect.left = x

# Classe dos sprites de vida 
class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('Assets/sprites/teste/live.png').convert_alpha() 
        self.image = pygame.transform.scale(self.image, (24,24))   
        self.rect = self.image.get_rect() 

        self.rect.top = y
        self.rect.left = x

# Classe Inimigo: Vespa
class Wasp(pygame.sprite.Sprite):
    def __init__(self):
        pass

# Classe Level (Inspirado de: https://www.youtube.com/watch?v=YWN8GcmJ-jA&t=1342s)
class Level:
    def __init__(self, level_data, surface):
        # Em qual superfície será colocado os tiles
        self.display_surface = surface
        # Chama a função setup_level (criar mapa)
        self.setup_level(level_data)

        # Lado do player para câmera
        self.side_x = screen_width/2
        self.zawarado = 0
        self.minx = 0
        self.maxx = 3072

    def setup_level(self, layout):
        # Level Setup
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.spikes = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.world_shift = 0

        # Verifica lista para criar o setup do mapa
        for linha_index, linha in enumerate(layout):  # Linha
            for tile_index, tile in enumerate(linha): # Coluna

                if tile != ' ':
                    # Coordenada X do tile no mapa
                    x = tile_index * tile_size
                    # Coordenada Y do tile no mapa
                    y = linha_index * tile_size
                
                # Tile
                if tile == 'X':
                    tile = Tile((x,y), tile_size)
                    self.tiles.add(tile) # Adiciona ao Grupo Tiles
                    groups['all_tiles'].add(tile)

                # Tile de fundo (embaixo do padrão)
                if tile == 'F':
                    tile = Tile_fundo((x,y), tile_size)
                    self.tiles.add(tile) # Adiciona ao Grupo Tiles
                    groups['all_tiles'].add(tile)

                # Player
                elif tile == 'M':
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)
                    

                # Espinho
                elif tile == 'E':
                    espinho = Espinho((x,y), tile_size)
                    self.spikes.add(espinho)

                # Caracol
                elif tile == 'C':
                    snail = Snail((x,y), tile_size)
                    self.enemies.add(snail)
                    groups["all_snails"].add(snail)
                
    def horizontal_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speedx

        hits = pygame.sprite.spritecollide(player, self.tiles, False)
        for sprite in hits:
            # Checa a colisão do player com um sprite
            if sprite.rect.colliderect(player.rect): 
                if player.direction.x > 0: 
                    # Player indo a direita, colide com lado esquerdo do sprite
                    player.rect.right = sprite.rect.left
                elif player.direction.x < 0: 
                    # Player indo a esquerda, colide com lado direito do sprite
                    player.rect.left = sprite.rect.right
    
    def vertical_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        hits = pygame.sprite.spritecollide(player, self.tiles, False)
        for sprite in hits:
            # Checa a colisão do player com um sprite
            if sprite.rect.colliderect(player.rect): 
                if player.direction.y > 0: 
                    # Player caindo, colide com o chão
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0      # Cancela a gravidade (evita uma catástrofe...)
                    player.can_jump = True
                    player.can_move = True
                elif player.direction.y < 0: 
                    # Player pulando, colide com o fundo do sprite
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0      # Macaco não fica preso no teto
    
    def player_hit_collision(self): # Colisão com hit ao player
        player = self.player.sprite
        
        # Tipos diferentes de hits
        #      Group Collide ou Sprite collide pra espinhos?
        hits_esp = pygame.sprite.spritecollide(player, self.spikes, False)
        hits_enemies = pygame.sprite.spritecollide(player, self.enemies, False)

        # Verifica se pode tomar hit
        self.hit_ticks = 5000
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde o último hit.
        elapsed_ticks = now - player.last_hit
        if elapsed_ticks > self.hit_ticks:
            # Marca o tick do hit
            player.last_hit = now

            # Colisão com espinhos
            for sprite in hits_esp:
                if sprite.rect.colliderect(player.rect): 
                    player.was_hit()
            pass
    
    def can_shift(self):
        self.zawarado -= self.world_shift
        pass

    def cam_scroll(self):
        player = self.player.sprite

        # Pega a posição do player e para onde vai
        self.direction_x = player.direction.x
        if self.direction_x > 0:
            self.side_x = player.rect.x + player.player_w
        elif self.direction_x < 0: 
            self.side_x = player.rect.x
        
        # Movimento da Camera
        if self.side_x >= screen_width * 3/4 and self.direction_x > 0 and self.zawarado < self.maxx - screen_width: #indo a direita
            self.world_shift = -8
            player.speedx = 0
        elif self.side_x <= screen_width/4 and self.direction_x < 0 and self.zawarado > self.minx: #indo a esquerda
            self.world_shift = 8
            player.speedx = 0
        else:
            self.world_shift = 0
            player.speedx = 6

    def run(self):
        # Level Tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.spikes.update(self.world_shift)
        self.spikes.draw(self.display_surface)

        # Inimigos
        self.enemies.update(self.world_shift)
        self.enemies.draw(self.display_surface)

        # Player
        self.player.update()
        self.horizontal_collision()
        self.player.draw(self.display_surface)
        self.vertical_collision()
        self.cam_scroll()
        self.can_shift()
                    

# Classe Tile (Tijolo/ Bloco do Chão)
class Tile(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()

        self.image = pygame.image.load('Assets/sprites/teste/tile.png')  # tiles
        self.image = pygame.transform.scale(self.image, (size,size))
        self.rect = self.image.get_rect(topleft = position)  
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, x_shift):    # Quando player chegar a uma parte do level, o level mexe para o lado (pygame é assim "press F")
        self.rect.x += x_shift

class Tile_fundo(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()

        self.image = pygame.image.load('Assets/sprites/teste/tile_fundo.png')  # tiles
        self.image = pygame.transform.scale(self.image, (size,size))
        self.rect = self.image.get_rect(topleft = position)  
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, x_shift):    # Quando player chegar a uma parte do level, o level mexe para o lado (pygame é assim "press F")
        self.rect.x += x_shift

# Classe spikes
class Espinho(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()

        self.image = pygame.Surface( (size, size) )
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft = position)
    
    def update(self, x_shift):    # Quando player chegar a uma parte do level, o level mexe para o lado (pygame é assim "press F")
        self.rect.x += x_shift