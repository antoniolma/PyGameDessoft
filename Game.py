# Jogo
import functions as f     # Importa as funções
import classes as c       # Importa as Classes
import pygame             # Importa biblioteca Pygame

# Inicializa o Pygame
pygame.init()

# ----- Gera tela principal
window = pygame.display.set_mode((1200, 900))
pygame.display.set_caption('Carlos, o macaco')

# ----- Inicia estruturas de dados
INICIO = 0
GAME = 1
QUIT = 2

game = INICIO

