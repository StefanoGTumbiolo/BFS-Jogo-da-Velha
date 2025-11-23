import collections
import random
import time

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

def imprimir_tabuleiro(t):
    print(f"\n {t[0]} | {t[1]} | {t[2]}")
    print("-----------")
    print(f" {t[3]} | {t[4]} | {t[5]}")
    print("-----------")
    print(f" {t[6]} | {t[7]} | {t[8]}\n")

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

    limite = 200000
    iteracoes = 0

    while fila and iteracoes < limite:
        iteracoes += 1

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

    return random.choice(movimentos)

# -------------------------------------------------
# Loop do jogo (interface)
# -------------------------------------------------

def jogo():
    tabuleiro = [' '] * 9
    jogador = 'X'       # humano
    ia = 'O'            # IA

    print("====================================")
    print("     JOGO DA VELHA — BFS IA")
    print("====================================")
    print("Você é X e joga primeiro.")
    print("Posições do tabuleiro:")
    print(" 0 | 1 | 2")
    print("-----------")
    print(" 3 | 4 | 5")
    print("-----------")
    print(" 6 | 7 | 8")
    print("====================================")

    while True:
        # Turno do jogador
        imprimir_tabuleiro(tabuleiro)
        jogada_valida = False

        while not jogada_valida:
            try:
                pos = int(input("Sua jogada (0-8): "))
                if pos in range(9) and tabuleiro[pos] == ' ':
                    tabuleiro[pos] = jogador
                    jogada_valida = True
                else:
                    print("Jogada inválida!")
            except ValueError:
                print("Digite um número entre 0 e 8.")

        # Vitória humana?
        if verificar_vitoria(tabuleiro, jogador):
            imprimir_tabuleiro(tabuleiro)
            print("🔥 Você venceu!!! 🔥")
            break

        if tabuleiro_cheio(tabuleiro):
            imprimir_tabuleiro(tabuleiro)
            print("😐 Empate!")
            break

        # Turno da IA
        print("\nIA pensando...")
        inicio = time.time()
        jogada_ia = bfs_melhor_jogada(tabuleiro, ia)
        fim = time.time()

        print(f"IA jogou na posição {jogada_ia} (tempo {fim - inicio:.5f}s)")

        tabuleiro[jogada_ia] = ia

        if verificar_vitoria(tabuleiro, ia):
            imprimir_tabuleiro(tabuleiro)
            print("💀 A IA venceu!")
            break

        if tabuleiro_cheio(tabuleiro):
            imprimir_tabuleiro(tabuleiro)
            print("😐 Empate!")
            break


# -------------------------------------------------
# Executar
# -------------------------------------------------

if __name__ == "__main__":
    jogo()
