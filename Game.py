# Jogo
from turtle import window_height
from assets import *        # Importa as funções
from level_class import *       # Importa as Classes
import pygame               # Importa biblioteca Pygame
from settings import *
from random import choice
from funcoes import *

# Inicializa o Pygame
pygame.init()

# ----- Gera tela principal
window = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Carlo's Delta Escape")
clock = pygame.time.Clock()
level = Level(level_map, window)

# ============ Inicia Assets ===========
assets['snail_death_sound'] = pygame.mixer.Sound('Assets/snail_sounds/CaracolDeath.mp3')
assets['player_jump_sounds'] = [pygame.mixer.Sound('Assets/player_sounds/MacacoPulo1.mp3'), pygame.mixer.Sound('Assets/player_sounds/MacacoPulo2.mp3')]
ganhou = False
player = level.player.sprite
score = player.score
lore_count = 1

# =========== Sons ============
pygame.mixer.music.load('assets/sounds/musiquinha-fundo.mp3')
pygame.mixer.music.set_volume(0.3)
snail_death_sound = assets['snail_death_sound']
player_jump_sounds = assets['player_jump_sounds']
pygame.mixer.init() 

# ----- Inicia estruturas de dados
INICIO = 0
LORE = 1
GAME = 2
GAME_OVER = 3
QUIT = 4
WIN = 5
COMMANDS = 6

game = INICIO

# Inicializando variáveis


# ===== Loop principal =====
pygame.mixer.music.play(loops=-1)

while game != QUIT:

    if game == INICIO or game == GAME_OVER or game == WIN or game == COMMANDS or game == LORE:
        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:                     
                    if game == COMMANDS:
                        game = INICIO

                if event.key == pygame.K_c:
                    if game == INICIO:
                        game = COMMANDS

                if event.key == pygame.K_x:
                    if game == LORE:
                        lore_count += 1
                        if lore_count == 7:
                            game = GAME

                if event.key == pygame.K_RETURN:
                    if game == GAME_OVER:
                        del level
                        level = Level(level_map, window)
                        score = 0
                        game = GAME
                    
                    if game == WIN:
                        del level
                        level = Level(level_map, window)
                        score = 0
                        game = GAME

                    if game == INICIO:
                        game = LORE

                    
            if event.type == pygame.QUIT:
                game = QUIT
        
        if game == INICIO: # se o jogo está na tela de inicio                             
            window.fill((0, 0, 0))
            window.blit(assets['tela de inicio'], (0, 0))
        
        elif game == LORE: # se o jogo está apresentando a cutscene 
            window.fill((0, 0, 0))
            if lore_count == 1:
                window.blit(assets['lore1'], (0, 0))
            elif lore_count == 2:
                window.blit(assets['lore2'], (0, 0))
            elif lore_count == 3:
                window.blit(assets['lore3'], (0, 0))
            elif lore_count == 4:
                window.blit(assets['lore4'], (0, 0))
            elif lore_count == 5:
                window.blit(assets['lore5'], (0, 0))
            elif lore_count == 6:
                window.blit(assets['lore6'], (0, 0))

        elif game == GAME_OVER: # se o jogo está na tela de inicio (player perdeu)    

            window.fill((0, 0, 0))  
            window.blit(assets['game over'], (0, 0))

        elif game == WIN: # se o jogo está na tela de vitória
            if score < 15000:
                window.fill((0, 0, 0))
                window.blit(assets['final ruim'], (0, 0))

                font = pygame.font.SysFont(None, 48)
                text = font.render('15.000', True, (255, 255, 255))
                text2 = font.render('{}'.format(score), True, (255, 255, 255))

                window.blit(text2, (100, 210))
                window.blit(text, (100, 320))
            else:
                window.fill((0, 0, 0))
                window.blit(assets['final bom'], (0, 0))

        elif game == COMMANDS: # se o jogo está na tela de comandos    
            window.fill((0, 0, 0))  
            window.blit(assets['comandos'], (0, 0))
        
    elif game == GAME: # se o jogo está rodando
       
        player = level.player.sprite

        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                game = QUIT 

        # ----- Jump Sound:
        if player.can_jump_sound:
            choice(assets['player_jump_sounds']).play()
            player.can_jump_sound = False
                        
        # ----- Player Info
        if player.hp <= 0 :#or len(caiu) > 0:
            game = GAME_OVER
            level.destroy()
            score = 0
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
            snail_death_sound.play()
            score += 2000
 
        # Verifica se o player chegou ao final do jogo (chegou no computador)
        chegou_final = pygame.sprite.spritecollide(player, level.totem, False, pygame.sprite.collide_mask)
        if len(chegou_final) > 0:
            ganhou = True
        
        # Tira ponto do player caso ele seja atingido 
        if player.dmg_score:
            score -= 500
            player.dmg_score = False

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
            level.destroy()

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

    clock.tick(60) 