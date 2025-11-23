import collections
import random

# -------------------------------------------------
# Funções básicas
# -------------------------------------------------

def verificar_vitoria(t, j):
    v = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    return any(t[a] == j and t[b] == j and t[c] == j for a,b,c in v)

def tabuleiro_cheio(t):
    return ' ' not in t

def obter_movimentos_validos(t):
    return [i for i in range(9) if t[i] == ' ']

# -------------------------------------------------
# BFS melhorada
# -------------------------------------------------

def bfs_melhor_jogada(tabuleiro, jogador_ia):
    jogador_humano = 'O' if jogador_ia == 'X' else 'X'
    movimentos = obter_movimentos_validos(tabuleiro)

    # 1 — vitória imediata
    for m in movimentos:
        t = tabuleiro[:]
        t[m] = jogador_ia
        if verificar_vitoria(t, jogador_ia):
            return m

    # 2 — bloquear vitória iminente do humano
    for m in movimentos:
        t = tabuleiro[:]
        t[m] = jogador_humano
        if verificar_vitoria(t, jogador_humano):
            return m

    # 3 — BFS real
    fila = collections.deque()
    visitados = set()

    for m in movimentos:
        t = tabuleiro[:]
        t[m] = jogador_ia
        fila.append((t, jogador_humano, m))

    while fila:
        estado, vez, primeira = fila.popleft()

        estado_tuple = tuple(estado)
        if estado_tuple in visitados:
            continue
        visitados.add(estado_tuple)

        if verificar_vitoria(estado, jogador_ia):
            return primeira

        if tabuleiro_cheio(estado):
            continue

        prox_vez = 'O' if vez == 'X' else 'X'

        for i in range(9):
            if estado[i] == ' ':
                novo = estado[:]
                novo[i] = vez
                fila.append((novo, prox_vez, primeira))

    # fallback
    return random.choice(movimentos)
