# Jogo
from turtle import window_height
from assets import *        # Importa as funções
from level_class import *       # Importa as Classes
import pygame               # Importa biblioteca Pygame
from settings import *

# Inicializa o Pygame
pygame.init()
load_assets()
pygame.mixer.music.load('assets/sounds/musiquinha-fundo.mp3')
pygame.mixer.music.set_volume(0.6)
pygame.mixer.init() 

# ----- Gera tela principal
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Carlos, o macaco')
clock = pygame.time.Clock()
level = Level(level_map, window)

# ============ Inicia Assets ===========
ja_foram = 0 

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
     
    if game == INICIO or game == GAME_OVER:
        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if game == GAME_OVER:
                        level = Level(level_map, window)
                    game = GAME
            if event.type == pygame.QUIT:
                game = QUIT
        
        if game == INICIO:
            font = pygame.font.SysFont(None, 48)
            text = font.render('Aperte SPACE para continuar', True, (255, 255, 255))

            # ----- Gera saídas
            window.fill((0, 100, 0))  # Preenche com a cor verde
            window.blit(text, (280, 230))

        elif game == GAME_OVER:
            font = pygame.font.SysFont(None, 48)
            text = font.render('Aperte SPACE para tentar novamente', True, (255, 0, 0))
            text2 = font.render('Game Over', True, (255, 0, 0))
            

            # Tela de Game Over
            window.fill( (255, 255, 255) )
            window.blit(text2, (280, 230))
            window.blit(text, (280, 280))
        
    elif game == GAME:
        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                game = QUIT                 
    
        # ----- Player Info
        if level.player.sprite.hp <= 0:
            game = GAME_OVER

        # Verifica se o caracol foi atingido pela banana - caso sim, ambos são deletados 
        hits = pygame.sprite.groupcollide(groups['all_bananas'], groups['all_tiles'] , True, False, pygame.sprite.collide_mask)

        # Verifica se a "bala" bateu no chão - se sim, ela é deletada
        hits = pygame.sprite.groupcollide(groups['all_bananas'], groups['all_snails'] , True, True, pygame.sprite.collide_mask)
        
        # for banana in hits:
        #     ja_foram += 1
        #     if ja_foram > 2:
        #         hits = pygame.sprite.groupcollide(groups['all_bananas'], groups['all_snails'] , False, True, pygame.sprite.collide_mask)
        
        # ----- Gera saídas
        window.fill((0, 0, 0))  # Preenche com a cor branca
        window.blit(assets['background'], (0, 0))
        level.run()
        all_sprites.update() 
        all_sprites.draw(window)


    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador
    
    clock.tick(60)