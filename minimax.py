import random

from jogo_da_velha import branco, token, verifica_ganhador, faz_movimento

score = {
    "EMPATE": 0,
    "X": 1,
    "O": -1
}

#função de posições
def getPosicoes(board):
    posicoes = []

    for i in range(3):
        for j in range(3):
            if (board[i][j] == branco):
                posicoes.append([i, j])
    
    return posicoes

#função de movimento da I.A.
def movimentoIA(board, jogador):
    possibilidades = getPosicoes(board)
    melhor_valor = None
    melhor_movimento = None

    for possibilidade in possibilidades:
        board[possibilidade[0]][possibilidade[1]] = token[jogador]
        valor = minimax(board, jogador)
        board[possibilidade[0]][possibilidade[1]] = branco

        if melhor_valor is None:
            melhor_valor = valor
            melhor_movimento = possibilidade
        elif jogador == 0:
            if (valor > melhor_valor):
                melhor_valor = valor
                melhor_movimento = possibilidade
        elif jogador == 1:
            if (valor < melhor_valor):
                melhor_valor = valor
                melhor_movimento = possibilidade

    return melhor_movimento[0], melhor_movimento[1]

#função de movimento da I.A. fácil (aleatória)
def movimentoIA_facil(board, jogador):
    posicoes = getPosicoes(board)
    i, j = random.choice(posicoes)
    faz_movimento(board, i, j, jogador)

#função de movimento da I.A. média (probabilística)
def movimentoIA_medio(board, jogador):
    if (random.random() < 0.5):
        i, j = movimentoIA(board, jogador)
        faz_movimento(board, i, j, jogador)
    else:
        movimentoIA_facil(board, jogador)

def minimax(board, jogador):
    ganhador = verifica_ganhador(board)

    if (ganhador):
        return score[ganhador]
    
    jogador = (jogador + 1) % 2

    possibilidades = getPosicoes(board)
    melhor_valor = None

    for possibilidade in possibilidades:
        board[possibilidade[0]][possibilidade[1]] = token[jogador]
        valor = minimax(board, jogador)
        board[possibilidade[0]][possibilidade[1]] = branco
        
        if melhor_valor is None:
            melhor_valor = valor
        elif jogador == 0:
            if (valor > melhor_valor):
                melhor_valor = valor
        elif jogador == 1:
            if (valor < melhor_valor):
                melhor_valor = valor
    
    return melhor_valor