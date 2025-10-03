import pygame
import constants
import helper

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

def pygameBoardLoop(BOARD_STATE, inQueue):
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                row = mouse_y//128
                col = mouse_x//128

                inQueue.put((row, col))

        screen.blit(background, (0, 0))

        for i in range(constants.BOARD_HEIGHT):
            for j in range(constants.BOARD_WIDTH):
                if BOARD_STATE[i][j] == '   ':
                    continue
                piece = img_dict[BOARD_STATE[i][j].strip()]
                rect = piece.get_rect(center=(128*j + 64, 128*i + 64))
                screen.blit(piece, rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()