from constants import *
import pygame
import sys

pygame.init()

size = Width, Height = 1024, 1024

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

background = pygame.transform.smoothscale(pygame.image.load('images/chess_background.png').convert(), (1024, 1024))

def load_piece(name, size=(128, 128)):
    img = pygame.image.load(f'images/{name}.png')
    return pygame.transform.smoothscale(img, size)

pieces = {
    "p": load_piece("bp"),
    "n": load_piece("bn"),
    "b": load_piece("bb"),
    "r": load_piece("br"),
    "q": load_piece("bq"),
    "k": load_piece("bk"),
    "P": load_piece("wp"),
    "N": load_piece("wn"),
    "B": load_piece("wb"),
    "R": load_piece("wr"),
    "Q": load_piece("wq"),
    "K": load_piece("wk"),
}

def Drawboard(BOARD):
    screen.blit(background, (0, 0))
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            if BOARD[i][j].strip() != '': 
                screen.blit(pieces[BOARD[i][j].strip()], (j*128, i*128))

    pygame.display.flip()