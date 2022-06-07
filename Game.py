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
pygame.mixer.music.set_volume(0.0)
pygame.mixer.init() 

# ----- Gera tela principal
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Carlo's Delta Escape")
clock = pygame.time.Clock()
level = Level(level_map, window)

# ============ Inicia Assets ===========
ganhou = False
player = level.player.sprite
score = player.score 

# ----- Inicia estruturas de dados
INICIO = 0
GAME = 1
GAME_OVER = 2
QUIT = 3
WIN = 4
COMMANDS = 5

game = INICIO

# Inicializando variáveis


# ===== Loop principal =====
pygame.mixer.music.play(loops=-1)

while game != QUIT:
     
     if game == INICIO or game == GAME_OVER or game == WIN or game == COMMANDS:
 
        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    if game == GAME_OVER:
                        ('entrou game_over')
                        del level
                        level = Level(level_map, window)
                    if game == WIN:

                        del level
                        level = Level(level_map, window)
                    game = GAME
                    if game == COMMANDS:
                        game = INICIO
                if event.key == pygame.K_c:
                    if game == INICIO:
                        game = COMMANDS
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

        elif game == WIN:

            window.fill((0, 0, 0))  # Preenche com a cor branca
            window.blit(assets['caracol'], (0, 0))

        elif game == COMMANDS:
            window.fill((0, 0, 0))  # Preenche com a cor branca
            window.blit(assets['comandos'], (0, 0))
        
     elif game == GAME:

        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                game = QUIT                 
    
        # ----- Player Info
        if player.hp <= 0 :#or len(caiu) > 0:

            level.destroy()
            score = 0
            game = GAME_OVER
            continue

        # Recarrega Munição
        if len(player.banana_storage) < 3:
            recharge_hits = pygame.sprite.spritecollide(player, level.recharge, True)
            for hit in recharge_hits:
                if len(player.banana_storage) > 0:
                    for b in player.banana_storage:
                        player.banana_storage.sprites()[-1].kill()
                score += 1000
                x = 30
                for i in range(3):
                    x += 30
                    balas_restantes = Munition(x, 10)
                    player.banana_storage.add(balas_restantes)
                    player.groups["all_sprites"].add(balas_restantes)

        # Verifica se o caracol foi atingido pela banana - caso sim, ambos são deletados 
        hits = pygame.sprite.groupcollide(groups['all_bananas'], groups['all_tiles'] , True, False, pygame.sprite.collide_mask)

        # Verifica se a "bala" bateu no chão - se sim, ela é deletada
        hits = pygame.sprite.groupcollide(groups['all_bananas'], groups['all_snails'] , True, True, pygame.sprite.collide_mask)
        if len(hits) > 0:
            score += 2000
 
        # Verifica se o player chegou ao final do jogo (chegou no computador)
        chegou_final = pygame.sprite.spritecollide(player, level.totem, False, pygame.sprite.collide_mask)
        if len(chegou_final) > 0:
            ganhou = True

        # printa Score
        font = pygame.font.SysFont(None, 48)
        score_text = font.render('{}'.format(score), True, (255, 255, 255))

        # ----- Gera saídas
        window.fill((0, 0, 0))                        # Preenche com a cor branca
        window.blit(assets['background'], (0, 0))
        window.blit(score_text, (65,80))
        level.run()
        all_sprites.update() 
        all_sprites.draw(window)

        if ganhou:
            game = WIN
            ganhou = False

    # ----- Atualiza estado do jogo
     pygame.display.update()  # Mostra o novo frame para o jogador
    
     clock.tick(60) 