# Jogo
import functions as f     # Importa as funções
import classes as c       # Importa as Classes
import pygame             # Importa biblioteca Pygame
from settings import level_map, tile_size, screen_width, screen_height

# Inicializa o Pygame
pygame.init()

# ----- Gera tela principal
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Carlos, o macaco')
clock = pygame.time.Clock()
level = c.Level(level_map, window)

# ----- Inicia estruturas de dados
INICIO = 0
GAME = 1
QUIT = 2

game = INICIO

# ===== Loop principal =====
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

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador