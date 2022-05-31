# Jogo
from turtle import window_height
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

all_sprites = groups['all_sprites']
all_bananas = groups['all_bananas']
all_snails = groups['all_snails'] 

assets = load_assets()

# ----- Inicia estruturas de dados
INICIO = 0
GAME = 1
GAME_OVER = 2
QUIT = 3

game = INICIO

# Inicializando variáveis


# ===== Loop principal =====
pygame.mixer.music.play(loops=-1000)

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
            
        font = pygame.font.SysFont(None, 48)
        text = font.render('Aperte SPACE para continuar', True, (255, 255, 255))

        # ----- Gera saídas
        window.fill((0, 100, 0))  # Preenche com a cor verde
        window.blit(text, (160, 356))
        
    elif game == GAME:
        
        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                game = QUIT                  
    
        # ----- Player Info
        #if player.hp <= 0:
        #   game = QUIT
        print(len(all_snails))
        hits = pygame.sprite.groupcollide(groups['all_bananas'], groups['all_snails'] , True, True, pygame.sprite.collide_mask)
        for banana in hits:
            print('pew')

        # ----- Gera saídas
        window.fill((0, 0, 0))  # Preenche com a cor branca
        window.blit(assets['background'], (0, 0))
        level.run()
        all_sprites.update() 
        all_sprites.draw(window)

    
    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador
    
    clock.tick(60)