import pygame
import constants
import helper
from queue import Empty

WIDTH = 1024
HEIGHT = 1024

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
background = pygame.transform.scale(pygame.image.load("imgs/chessboard.png"), (WIDTH, HEIGHT))

img_dict = {
    "b": pygame.transform.scale(pygame.image.load("imgs/bb.png"), (WIDTH//8, HEIGHT//8)),
    "B": pygame.transform.scale(pygame.image.load("imgs/wb.png"), (WIDTH//8, HEIGHT//8)),
    "n": pygame.transform.scale(pygame.image.load("imgs/bn.png"), (WIDTH//8, HEIGHT//8)),
    "N": pygame.transform.scale(pygame.image.load("imgs/wn.png"), (WIDTH//8, HEIGHT//8)),
    "q": pygame.transform.scale(pygame.image.load("imgs/bq.png"), (WIDTH//8, HEIGHT//8)),
    "Q": pygame.transform.scale(pygame.image.load("imgs/wq.png"), (WIDTH//8, HEIGHT//8)),
    "k": pygame.transform.scale(pygame.image.load("imgs/bk.png"), (WIDTH//8, HEIGHT//8)),
    "K": pygame.transform.scale(pygame.image.load("imgs/wk.png"), (WIDTH//8, HEIGHT//8)),
    "p": pygame.transform.scale(pygame.image.load("imgs/bp.png"), (WIDTH//8, HEIGHT//8)),
    "P": pygame.transform.scale(pygame.image.load("imgs/wp.png"), (WIDTH//8, HEIGHT//8)),
    "r": pygame.transform.scale(pygame.image.load("imgs/br.png"), (WIDTH//8, HEIGHT//8)),
    "R": pygame.transform.scale(pygame.image.load("imgs/wr.png"), (WIDTH//8, HEIGHT//8))
}

def highlight_squares(screen, moves, color=(0, 255, 0), alpha=100):
    highlight_surface = pygame.Surface((128, 128), pygame.SRCALPHA)
    highlight_surface.fill((*color, alpha))

    for (row, col) in moves:
        x = col * 128
        y = row * 128
        screen.blit(highlight_surface, (x, y))

def pygameBoardLoop(BOARD_STATE, inQueue, game, MoveListQueue):
    clock = pygame.time.Clock()
    running = True

    current_highlight = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or game == False:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    row = mouse_y//128
                    col = mouse_x//128

                    inQueue.put((row, col))
                elif event.button == 3:
                    inQueue.put((-1, -1))
                    current_highlight = None

        try:
            MoveList = MoveListQueue.get_nowait()
            current_highlight = MoveList
        except Empty:
            MoveList = None

        screen.blit(background, (0, 0))

        for i in range(constants.BOARD_HEIGHT):
            for j in range(constants.BOARD_WIDTH):
                if BOARD_STATE[i][j] == '   ':
                    continue
                piece = img_dict[BOARD_STATE[i][j].strip()]
                rect = piece.get_rect(center=(128*j + 64, 128*i + 64))
                screen.blit(piece, rect)
        
        if current_highlight:
            highlight_squares(screen, current_highlight)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()