import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pygame

from jogo_da_velha import criar_board, faz_movimento, get_input_valido, \
    print_board, verifica_ganhador, verica_movimento

from minimax import movimentoIA, movimentoIA_facil, movimentoIA_medio

pygame.mixer.init()
pygame.mixer.music.load('musica.mp3')
pygame.mixer.music.play()

pygame.font.init()

dificuldades = {
    1: "Facil",
    2: "Medio",
    3: "Dificil",
}

def draw_board(win, board):
    height = 600
    width = 600
    tamanho = 600/3

    for i in range(1, 3):
        pygame.draw.line(win, (0, 0, 0), (0, i * tamanho),\
                              (width, i * tamanho), 3)
        
        pygame.draw.line(win, (0, 0, 0), (i * tamanho, 0), \
                         (i * tamanho, height), 3)
        
    for i in range(3):
        for j in range(3):
            font = pygame.font.SysFont('comicsans', 100)

            x = j * tamanho
            y = i * tamanho

            text = font.render(board[i][j], 1, (0,0,0))
            win.blit(text, ((x + 75), (y + 75)))

def draw_dificuldade(win, dificuldade):
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render("Nivel: " + dificuldades[dificuldade], 1, (255, 255, 255))
    win.blit(text, (10, 10))

def redraw_window(win, board, dificuldade):
    win.fill((25, 42, 86))
    draw_board(win, board)
    draw_dificuldade(win, dificuldade)

def escolhe_dificuldade(win):
    font = pygame.font.SysFont('comicsans', 40)

    win.fill((25, 42, 86))
    win.blit(font.render("Escolha a dificuldade", 1, (255, 255, 255)), (110, 120))
    win.blit(font.render("1 - Facil", 1, (255, 255, 255)), (220, 240))
    win.blit(font.render("2 - Medio", 1, (255, 255, 255)), (220, 310))
    win.blit(font.render("3 - Dificil", 1, (255, 255, 255)), (220, 380))
    pygame.display.update()

    while(True):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                return None
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_1):
                    return 1
                elif (event.key == pygame.K_2):
                    return 2
                elif (event.key == pygame.K_3):
                    return 3

def mostra_resultado(win, board, dificuldade, ganhador):
    redraw_window(win, board, dificuldade)

    font = pygame.font.SysFont('comicsans', 50)

    if (ganhador == "EMPATE"):
        mensagem = "Empate!"
    else:
        mensagem = "Vencedor: " + ganhador

    win.blit(font.render(mensagem, 1, (255, 255, 255)), (170, 250))
    win.blit(font.render("Pressione uma tecla", 1, (255, 255, 255)), (90, 320))
    win.blit(font.render("para voltar ao menu", 1, (255, 255, 255)), (90, 380))
    pygame.display.update()

    while(True):
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                return False
            elif (event.type == pygame.KEYDOWN):
                return True

def main():
    win = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Jogo da Velha")

    while(True):
        dificuldade = escolhe_dificuldade(win)

        if (dificuldade is None):
            return

        board = criar_board()

        redraw_window(win, board, dificuldade)
        pygame.display.update()

        jogador = 0
        ganhador = verifica_ganhador(board)

        while(not ganhador):
            i = None
            j = None
            print_board(board)

            if jogador == 0:
                jogou = False

                while(not jogou):
                    for event in pygame.event.get():
                        if (event.type == pygame.QUIT):
                            return
                        elif (event.type == pygame.MOUSEBUTTONUP):
                            tamanho = 600/3

                            pos = pygame.mouse.get_pos()
                            i = int(pos[1]/tamanho)
                            j = int(pos[0]/tamanho)
                            jogou = True

                if verica_movimento(board, i, j):
                    faz_movimento(board, i, j, jogador)
                    jogador = (jogador + 1) % 2
            else:
                if (dificuldade == 1):
                    movimentoIA_facil(board, jogador)
                elif (dificuldade == 2):
                    movimentoIA_medio(board, jogador)
                else:
                    i, j = movimentoIA(board, jogador)
                    faz_movimento(board, i, j, jogador)

                jogador = (jogador + 1) % 2

            ganhador = verifica_ganhador(board)
            redraw_window(win, board, dificuldade)
            pygame.display.update()

        if (not mostra_resultado(win, board, dificuldade, ganhador)):
            return

main()