import pygame               # Importa biblioteca Pygame
from settings import screen_height, screen_width

# Funções para o Jogo

PLAYER = 'player'

groups = {}  # Inicializa diionário que conterá os grupos de sprites
assets = {}

def load_assets():
        # Carregando todos os sprites
    assets['background'] = pygame.image.load('Assets/sprites/teste/fundo_completo1.png')
    assets['background'] = pygame.transform.scale(assets['background'], (screen_width, screen_height))

    assets[PLAYER] = pygame.image.load('Assets/sprites/teste/el mamaco parado.png')
    assets['player_virado'] = pygame.image.load('Assets/sprites/teste/mamaco_virado.png')

    assets['caracol'] = pygame.image.load('Assets/sprites/teste/el caracol.png')

    assets['balas'] = pygame.image.load('Assets/sprites/teste/banana munição.png')

    assets['municao_disponivel'] = pygame.image.load('Assets/sprites/teste/municao.png')

    assets['municao_disponivel'] = pygame.image.load('Assets/sprites/teste/tile.png')

    assets['comandos'] = pygame.image.load('Assets/sprites/teste/tela de comandos.png')

      # Carregando os sons

    pygame.mixer.music.load('assets/sounds/musiquinha-fundo.mp3')
    pygame.mixer.music.set_volume(0.6)

    return assets
