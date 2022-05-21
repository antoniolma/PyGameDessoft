import pygame
from settings import level_map, screen_height, tile_size, screen_width

# Classe do Carlos, o Macaco
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        [player_w, player_h] = [ tile_size, tile_size ]   # player size
        
        self.image = pygame.image.load('Assets/sprites/personagens/teste_macaco.png')  #player img
        self.rect = self.image.get_rect(topleft = pos)  
        self.image = pygame.transform.scale(self.image, (player_w, player_h))   # Rescale the player

# Classe Inimigo: Caracol
class Snail(pygame.sprite.Sprite):
    def __init__(self):
        pass

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
        
        # Load Images
        # floor_img = pygame.image.load('')

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

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
                
            
    def run(self):
        # Level Tiles
        self.tiles.draw(self.display_surface)

        # Player
        self.player.draw(self.display_surface)
                    

# Classe Tile (Tijolo/ Bloco do Chão)
class Tile(pygame.sprite.Sprite)    :
    def __init__(self, position, size):
        super().__init__()

        self.image = pygame.Surface( (size, size)  ) # Cria um retângulo
        self.image.fill('green')
        self.rect = self.image.get_rect(topleft = position)