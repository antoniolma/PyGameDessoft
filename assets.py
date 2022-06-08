import pygame               # Importa biblioteca Pygame
from settings import screen_height, screen_width

# Funções para o Jogo

PLAYER = 'player'

groups = {}  # Inicializa dicionário que conterá os grupos de sprites
assets = {}


# ===========  Carregando todos os sprites  =============
# --- Fundo:
assets['background'] = pygame.image.load('Assets/sprites/teste/fundo_completo1.png')
assets['background'] = pygame.transform.scale(assets['background'], (screen_width, screen_height))

# --- Player:
assets[PLAYER] = pygame.image.load('Assets/sprites/teste/el mamaco parado.png')
assets['player_virado'] = pygame.image.load('Assets/sprites/teste/mamaco_virado.png')
assets['player_hitado_right'] = pygame.image.load('Assets/sprites/teste/monkey_righthit.png')
assets['player_hitado_left'] = pygame.image.load('Assets/sprites/teste/monkey_lefthit.png')

# --- Inimigos:
assets['caracol'] = pygame.image.load('Assets/sprites/teste/el caracol.png')

# --- Vida:
assets['heart'] = pygame.image.load('Assets/sprites/teste/live.png')

# --- Munição:
assets['balas'] = pygame.image.load('Assets/sprites/teste/banana munição.png')
assets['municao'] = pygame.image.load('Assets/sprites/teste/municao.png')

# --- Tiles:
assets['tile_grama'] = pygame.image.load('Assets/sprites/teste/tile.png')
assets['tile_fundo'] = pygame.image.load('Assets/sprites/teste/tile_fundo.png')
assets['tile_inv'] = pygame.image.load('Assets/sprites/teste/tile_transp.png')

# --- Telas:
assets['comandos'] = pygame.image.load('Assets/sprites/teste/tela de comandos.png')
assets['tela de inicio'] = pygame.image.load('Assets/sprites/teste/tela inicial.jpeg')
assets['game over'] = pygame.image.load('Assets/sprites/teste/game over.jpeg')

# --- Objetivo:
assets['computer'] = pygame.image.load('Assets/sprites/teste/final.png')  
