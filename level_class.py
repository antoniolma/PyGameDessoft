from os import kill
import pygame
from settings import level_map, screen_height, tile_size, screen_width
from player_class import *
from enemy_class import *
from assets import *

all_bananas = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_snails = pygame.sprite.Group()
all_tiles = pygame.sprite.Group()
invisible_tiles = pygame.sprite.Group()
move_tiles = pygame.sprite.Group()
groups['all_sprites'] = all_sprites
groups['all_bananas'] = all_bananas
groups['all_snails'] = all_snails
groups['all_tiles'] = all_tiles
groups['invisible_tiles'] = invisible_tiles
groups['move_tiles'] = move_tiles

was_hit = []

# Classe Level (Inspirado de: https://www.youtube.com/watch?v=YWN8GcmJ-jA&t=1342s)
class Level:
    def __init__(self, level_data, surface):
        # Em qual superfície será colocado os tiles
        self.display_surface = surface
        # Chama a função setup_level (criar mapa)
        self.setup_level(level_data)

        # Lado do player para câmera
        self.side_x = screen_width/2
        self.zawarudo = 0
        self.minx = 0
        self.maxx = 10624
        self.p = None

    def setup_level(self, layout):
        # Grupos do level
        self.tiles = pygame.sprite.Group()
        self.invisible = pygame.sprite.Group()
        self.spikes = pygame.sprite.Group()
        self.totem = pygame.sprite.Group()

        # Grupos do player
        self.player = pygame.sprite.GroupSingle()
        self.recharge = pygame.sprite.Group()
        
        # Grupos de inimigos
        self.snail = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Movimento DO LEVEL
        self.world_shift = 0
        
        # Last hit no player
        self.last = 0

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

                # Tile de fundo (embaixo da grama)
                if tile == 'F':
                    tile = Tile_fundo((x,y), tile_size)
                    self.tiles.add(tile) # Adiciona ao Grupo Tiles
                    groups['all_tiles'].add(tile)

                # Tile para parar o caracol
                if tile == 'T':
                    tile = Tile_t((x,y), tile_size)
                    self.invisible.add(tile)
                    groups['invisible_tiles'].add(tile)

                if tile == 'V':
                    tile = Tile_move((x,y), tile_size)
                    self.tiles.add(tile)
                    groups['move_tiles'].add(tile)

                # Player
                elif tile == 'M':
                    player_sprite = Player((x,y))
                    self.p = player_sprite
                    self.player.add(player_sprite)
                    
                # Espinho
                elif tile == 'E':
                    espinho = Espinho((x,y), tile_size)
                    self.spikes.add(espinho)

                # Caracol
                elif tile == 'C':
                    snail = Snail((x,y), tile_size)
                    self.snail.add(snail)
                    self.enemies.add(snail)
                    groups["all_snails"].add(snail)
                
                # Recarga Munição
                elif tile == 'A':
                    ammo = Recharge( (x,y), tile_size)
                    self.recharge.add(ammo)

                # Totem final do jogo
                elif tile == 'O':
                    pc = Computer( (x,y), tile_size)
                    self.totem.add(pc)
                
    def horizontal_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speedx

        # Horizontal Collision with tile
        tile_hits = pygame.sprite.spritecollide(player, self.tiles, False)
        for sprite in tile_hits:
            # Checa a colisão do player com um sprite
            if sprite.rect.colliderect(player.rect): 
                if player.direction.x > 0: 
                    # Player indo a direita, colide com lado esquerdo do sprite
                    player.rect.right = sprite.rect.left
                elif player.direction.x < 0: 
                    # Player indo a esquerda, colide com lado direito do sprite
                    player.rect.left = sprite.rect.right

        if player.rect.top > screen_height:
            player.hp -= 3

        # Horizontal Collision with enemies
        for enemy in self.enemies:
            if pygame.sprite.collide_mask(enemy, player):
                self.player_hit_time()
                # player.gethit_jump()
                if player.direction.x > 0: 
                    # Player indo a direita, colide com lado esquerdo do sprite
                    player.rect.right == enemy.rect.left
                elif player.direction.x < 0: 
                    # Player indo a esquerda, colide com lado direito do sprite
                    player.rect.left == enemy.rect.right

        spike_hits = pygame.sprite.spritecollide(player, self.spikes, False)
        for spike in spike_hits:
            if spike.rect.colliderect(player.rect):
                self.player_hit_time()

                # Colisão Horizontal
                if player.direction.x > 0: 
                    # Player indo a direita, colide com lado esquerdo do sprite
                    player.rect.right = spike.rect.left
                elif player.direction.x < 0: 
                    # Player indo a esquerda, colide com lado direito do sprite
                    player.rect.left = spike.rect.right

    def vertical_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        # Vert. Collision with Tiles
        tile_hits = pygame.sprite.spritecollide(player, self.tiles, False)
        for sprite in tile_hits:
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

        # # Vert. Collision with enemies
        # self.e_hits = pygame.sprite.spritecollide(player, self.enemies, False)
        # for sprite in self.e_hits:
        #     # Checa a colisão do player com um sprite
        #     if sprite.rect.colliderect(player.rect):
                
        # Colisão com inimigo
        e_hits = pygame.sprite.spritecollide(player, self.enemies, False)
        for enemy in e_hits:
            if pygame.sprite.collide_mask(enemy, player):
                self.player_hit_time()
                # player.gethit_jump()
                if player.direction.y > 0: 
                    # Player caindo, colide com o chão
                    player.direction.y = 0      # Cancela a gravidade (evita uma catástrofe...)
                    player.can_jump = True
                    player.can_move = True
                elif player.direction.y < 0: 
                    # Player pulando, colide com o fundo do sprite
                    player.direction.y = 0      # Macaco não fica preso no teto
                if player.hp != 3:
                    enemy.kill()

        # Colisão com espinhos
        spike_hits = pygame.sprite.spritecollide(player, self.spikes, False)
        for spike in spike_hits:
            if spike.rect.colliderect(player.rect):
                self.player_hit_time()
                
                if player.direction.y > 0: 
                    # Player caindo, colide com o chão
                    player.rect.bottom = spike.rect.top
                    player.direction.y = 0      # Cancela a gravidade (evita uma catástrofe...)
                    player.can_jump = True
                    player.can_move = True
                elif player.direction.y < 0: 
                    # Player pulando, colide com o fundo do sprite
                    player.rect.top = spike.rect.bottom
                    player.direction.y = 0      # Macaco não fica preso no teto

    def last_hit(self):
        self.last = pygame.time.get_ticks()

    def player_hit_time(self): # Colisão com hit ao player
        player = self.player.sprite
        player.last_hit = pygame.time.get_ticks()
        player.was_hit = True

        # Verifica se pode tomar hit
        self.hit_ticks = 1000
        now = pygame.time.get_ticks()

        # Verifica quantos ticks se passaram desde o último hit.
        elapsed_ticks = now - self.last
        if elapsed_ticks >= self.hit_ticks:
            self.last_hit()
            player.live.sprites()[-1].kill()
            player.hp -= 1 
            was_hit.append(1)
    
    def can_shift(self):
        self.zawarudo -= self.world_shift
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
        if self.side_x >= screen_width * 3/4 and self.direction_x > 0 and self.zawarudo < self.maxx - screen_width: #indo a direita
            self.world_shift = -8
            player.speedx = 0
        elif self.side_x <= screen_width/4 and self.direction_x < 0 and self.zawarudo > self.minx: #indo a esquerda
            self.world_shift = 8
            player.speedx = 0
        else:
            self.world_shift = 0
            player.speedx = 6

    def destroy(self):
        for s in self.tiles.sprites():
            s.kill()
        for s in self.invisible.sprites():
            s.kill()
        for s in self.spikes.sprites():
            s.kill()
        for s in self.totem.sprites():
            s.kill()
        for s in self.player.sprites():
            s.kill()
        for s in self.recharge.sprites():
            s.kill()
        for s in self.snail.sprites():
            s.kill()
        for s in self.enemies.sprites():
            s.kill()
        for s in all_sprites.sprites():
            s.kill()
        for s in groups["all_snails"]:
            s.kill()
        was_hit = []
        

    def run(self):
        # Level Tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.invisible.update(self.world_shift)
        self.invisible.draw(self.display_surface)
        self.spikes.update(self.world_shift)
        self.spikes.draw(self.display_surface)
        self.recharge.update(self.world_shift)
        self.recharge.draw(self.display_surface)
        self.totem.update(self.world_shift)
        self.totem.draw(self.display_surface)

        # Inimigos
        self.snail.update(self.world_shift)
        self.snail.draw(self.display_surface)

        # Player
        self.player.update()
        self.horizontal_collision()
        self.player.draw(self.display_surface)
        self.vertical_collision()
        self.cam_scroll()
        self.can_shift()
        
                    
# ==============================================================================================================================================================================

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
        
    def update(self, x_shift):    
        self.rect.x += x_shift

class Tile_t(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()

        self.image = pygame.image.load('Assets/sprites/teste/tile_transp.png')  # tiles
        self.image = pygame.transform.scale(self.image, (size,size))
        self.rect = self.image.get_rect(topleft = position)  
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, x_shift):    
        self.rect.x += x_shift

class Tile_move(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()

        self.image = pygame.image.load('Assets/sprites/teste/tile.png').convert_alpha() # tiles
        self.image = pygame.transform.scale(self.image, (size,size))
        self.rect = self.image.get_rect(topleft = position)  
        self.mask = pygame.mask.from_surface(self.image)

        self.speedx = -4
    
    def tile_moviment(self):
        collision_tile_inv = pygame.sprite.groupcollide(groups['move_tiles'], groups['invisible_tiles'], False, False)

        for move_tile, tiles in collision_tile_inv.items():
            bloco = tiles[0]
            # Caracol indo para direita
            if bloco.rect.right > move_tile.rect.right > bloco.rect.left:
                move_tile.rect.right = bloco.rect.left
                move_tile.speedx = -move_tile.speedx

            # Caracol indo para esquerda
            elif bloco.rect.left < move_tile.rect.left < bloco.rect.right:
                move_tile.rect.left = bloco.rect.right
                move_tile.speedx = -move_tile.speedx

    def update(self, x_shift):    # Quando player chegar a uma parte do level, o level mexe para o lado (pygame é assim "press F")
        self.rect.x += x_shift + self.speedx
        self.tile_moviment()

# ==============================================================================================================================================================================

# Classe Recarga Munição
class Recharge(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()

        self.image = pygame.image.load('Assets/sprites/teste/municao.png')  
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = position)
    
    def update(self, x_shift):    # Quando player chegar a uma parte do level, o level mexe para o lado 
        self.rect.x += x_shift

# ==============================================================================================================================================================================

# Classe do totem de finalização (nota na Delta)
class Computer(pygame.sprite.Sprite):
    def __init__(self, position, size):
        super().__init__()

        self.image = pygame.image.load('Assets/sprites/teste/final.png')  
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft = position)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, x_shift):  
        self.rect.x += x_shift
    