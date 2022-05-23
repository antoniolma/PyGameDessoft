# Jogo
from functions import *     # Importa as funções
from classes import *       # Importa as Classes
import pygame               # Importa biblioteca Pygame
from settings import *

# Inicializa o Pygame
pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Carlos, o macaco')
clock = pygame.time.Clock()
level = Level(level_map, window)

# ============ Inicia Assets ===========
player = Player((192, 576))
pygame.mixer.music.load('assets/sounds/musiquinha-fundo.mp3')
pygame.mixer.music.set_volume(0.4)

# ----- Inicia estruturas de dados
INICIO = 0
GAME = 1
QUIT = 2

game = INICIO

# ===== Loop principal =====
pygame.mixer.music.play()

while game != QUIT:
    
    if game == INICIO:
        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_SPACE:
                    game = GAME
            if event.type == pygame.QUIT:
                game = QUIT
        
        # ----- Gera saídas
        window.fill((0, 100, 0))  # Preenche com a cor verde
        
    elif game == GAME:
        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                game = QUIT           

        # ----- Gera saídas
        window.fill((59, 131, 189))  # Preenche com a cor azul
        level.run()

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador
    clock.tick(60)