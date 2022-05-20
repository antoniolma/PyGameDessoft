import pygame
from settings import level_map, screen_height, tile_size, screen_width

# Classe do Carlos, o Macaco
class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        

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

        # Verifica lista para criar o setup do mapa
        for linha_index, linha in enumerate(layout):  # Linha
            for tile_index, tile in enumerate(linha): # Coluna

                # Coordenada X do tile no mapa
                self.x = linha_index
                # Coordenada Y do tile no mapa
                self.y = tile_index
                
                if tile == 'X':
                    pass
                elif tile == 'M':
                    pass
                    

# Classe Tile (Tijolo/ Bloco do Chão)
class Tile:
    def __init__(self):
        pass