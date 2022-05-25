import pygame
from settings import level_map, screen_height, tile_size, screen_width

groups = {}

def municao_gasta(groups):
    municao = 3

    for i in range(len( groups['all_bananas'])):
        municao -= 1

    return municao

# Classe do Carlos, o Macaco
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        [player_w, player_h] = [ tile_size, tile_size ]   # player size
        
        self.image = pygame.image.load('Assets/sprites/teste/el mamaco parado.png').convert_alpha()  #player img 
        self.image = pygame.transform.scale(self.image, (player_w, player_h))   # Rescale the player
        self.rect = self.image.get_rect(topleft = pos)
        self.rect.left = player_w
        self.rect.centery = player_h / 2
        self.groups = groups

        # Mercando de quanto em quanto tempo é possível atirar
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 500
        
        # Movimente
        self.direction = pygame.math.Vector2(0,0)  # Cria um Vetor2 (2 dimensões) (lista de valores x e y)
        self.speedx = 4
        self.gravity = 0.8
        self.jump_speed = -12

    # Pega as teclas pressionadas relacionadas ao player
    def get_input(self):
        keys = pygame.key.get_pressed()

        # Movimento pros lados
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        
        # Movimento pulo
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.jump()

        # Atirar
        if keys[pygame.K_SPACE]:
            municao = municao_gasta(groups)
            print(municao)
            self.shoot(municao)
        
        # Não permite personagem sair da tela
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.left < 0:
            self.rect.left = 0
         
        # if keys[pygame.K_RCTRL]:
        #     self.draw()

    # Gravidade sobre o player
    def apply_gravity(self):
        if self.direction.y >= 32:
            self.direction.y = 32
        self.direction.y += self.gravity  # Todo frame desce 0.8 em Y
        self.rect.y += self.direction.y   # O retângulo do player se move

    def jump(self):
        self.direction.y = self.jump_speed

    def shoot(self, municao):
        # Verifica se pode atirar
        now = pygame.time.get_ticks()
        # Verifica quantos ticks se passaram desde o último tiro.
        elapsed_ticks = now - self.last_shot

        # Se já pode atirar novamente...
        if elapsed_ticks > self.shoot_ticks and municao > 0:
            # Marca o tick da nova imagem.
            self.last_shot = now
            # Criando nova banana
            bananinha = Banana(self.rect.centery, self.rect.right)
            self.groups['all_sprites'].add(bananinha)
            self.groups['all_bananas'].add(bananinha)

    # ferramenta de Debug (mostra grid de tiles e macaco)
    # def draw(self):
    #     for tile in Level.tiles:
    #         Level.display_surface.blit(tile.image, tile.rect)
    #         pygame.draw.rect(Level.display_surface, (255, 255, 255), tile.rect, 2)
    #     Level.display_surface.blit(self.image, self.rect)
    #     pygame.draw.rect(Level.display_surface, (255, 255, 255), self.rect, 2)
    
    # Atualiza o player
    def update(self):
        self.get_input()
        # self.draw()

# Classe Inimigo: Caracol
class Snail(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('Assets/sprites/teste/el caracol.png').convert_alpha()  #player img 
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size ))   # Rescale the player
        self.rect = self.image.get_rect() 

        pass

# Classe do tiro
class Banana(pygame.sprite.Sprite):
    def __init__(self, centery, rightplayer):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load('Assets/sprites/teste/banana munição.png').convert_alpha()  #player img 
        self.image = pygame.transform.scale(self.image, (tile_size, tile_size ))   # Rescale the player
        self.rect = self.image.get_rect() 

        self.rect.centery = centery + 15
        self.rect.left = rightplayer - 35
        self.speedx = 10

    def update(self):
        # A bala só se move no eixo x
        self.rect.x += self.speedx

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

    def setup_level(self, layout):
        # Level Setup
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.world_shift = 0

        # Verifica lista para criar o setup do mapa
        for linha_index, linha in enumerate(layout):  # Linha
            for tile_index, tile in enumerate(linha): # Coluna

                # Coordenada X do tile no mapa
                x = tile_index * tile_size
                # Coordenada Y do tile no mapa
                y = linha_index * tile_size
                
                if tile == 'X':     # Chão
                    tile = Tile((x,y), tile_size)
                    self.tiles.add(tile) # Adiciona ao Grupo Tiles
                elif tile == 'M':   # Macaco
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)
                
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
                elif player.direction.y < 0: 
                    # Player pulando, colide com o fundo do sprite
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0      # Macaco não fica preso no teto

    def run(self):
        # Level Tiles
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)

        # Player
        self.player.update()
        self.horizontal_collision()
        self.player.draw(self.display_surface)
        self.vertical_collision()
                    

# Classe Tile (Tijolo/ Bloco do Chão)
class Tile(pygame.sprite.Sprite)    :
    def __init__(self, position, size):
        super().__init__()

        # self.image = pygame.Surface( (size, size) )
        # self.image.fill('green')
        self.image = pygame.image.load('Assets/sprites/teste/tile.png')  # tiles
        self.image = pygame.transform.scale(self.image, (size,size))
        self.rect = self.image.get_rect(topleft = position)  
        

    def update(self, x_shift):    # Quando player chegar a uma parte do level, o level mexe para o lado (pygame é assim "press F")
        self.rect.x += x_shift