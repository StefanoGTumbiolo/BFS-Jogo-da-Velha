import collections
import random
import time

# ------------------------------------------------------------------------------
# LÓGICA GERAL
# ------------------------------------------------------------------------------

# [X] CLASSE OU ESTRUTURA DO JOGO
#     Contém o estado do tabuleiro, como uma lista simples de 9 strings aonde cada posição pode ser ' ', 'X' ou 'O'.

# [X] FUNÇÃO: inicializar_tabuleiro()
#     - Retorna uma lista [' ', ' ', ..., ' '] de 9 posições.
def inicializar_tabuleiro():
    return [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

# [X] FUNÇÃO: fazer_jogada(tabuleiro, posicao, jogador)
#     - Recebe o tabuleiro.
#     - Verifica se a posição é válida (se estiver vazia e dentro do range).
#     - Insere 'X' ou 'O' (jogador) na posição.
#     - Retorna True se funcionou, False se inválido.
def fazer_jogada(tabuleiro, posicao, jogador):
    if posicao < 0 or posicao > 8:
        return False
    
    if tabuleiro[posicao] == ' ':
        tabuleiro[posicao] = jogador
        return True
    
    return False

# [X] FUNÇÃO: verificar_vitoria(tabuleiro, jogador)
#     - Verifica as 3 linhas, 3 colunas e 2 diagonais.
#     - Retorna True se o jogador venceu, ou seja, se há 3 símbolos iguais em linha, coluna ou diagonal.
def verificar_vitoria(tabuleiro, jogador):
    combinacoes_vitoria = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8), 
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)             
    ]
    
    for a, b, c in combinacoes_vitoria:
        if tabuleiro[a] == jogador and tabuleiro[b] == jogador and tabuleiro[c] == jogador:
            return True
    
    return False

# [X] FUNÇÃO: tabuleiro_cheio(tabuleiro)
#     - Verifica se não há mais espaços vazios (vai acontecer se o jogo terminou em empate).
def tabuleiro_cheio(tabuleiro):
    if ' ' not in tabuleiro:
        return True
    return False

# [X] FUNÇÃO: obter_movimentos_validos(tabuleiro)
#     - Retorna uma lista de índices (0-8) que estão vazios.
#     - Vai ser usada pela IA para saber onde pode jogar.
def obter_movimentos_validos(tabuleiro):
    validos = []
    for i in range(9):
        if tabuleiro[i] == ' ':
            validos.append(i)
    return validos

# [X] FUNÇÃO: imprimir_tabuleiro(tabuleiro)
#     - Mostra o estado atual do jogo no terminal durante a vez do jogador humano.
def imprimir_tabuleiro(tabuleiro):
    print(f"{tabuleiro[0]} | {tabuleiro[1]} | {tabuleiro[2]}")
    print("--+---+--")
    print(f"{tabuleiro[3]} | {tabuleiro[4]} | {tabuleiro[5]}")
    print("--+---+--")
    print(f"{tabuleiro[6]} | {tabuleiro[7]} | {tabuleiro[8]}")

# ------------------------------------------------------------------------------
# USO DA BFS
# ------------------------------------------------------------------------------

# [X] FUNÇÃO: bfs_melhor_jogada(jogo, jogador_ia)
#     - Implementa a lógica da IA usando BFS para decidir a melhor jogada.
#     - Retorna o índice (0-8) da melhor jogada para a IA.
def bfs_melhor_jogada(tabuleiro, jogador_ia):
    jogador_humano = 'X' if jogador_ia == 'O' else 'O'
    
    if tabuleiro_cheio(tabuleiro):
        return None
    
    movimentos_validos = obter_movimentos_validos(tabuleiro)
    
    # Heurística - Vitória imediata da IA
    for movimento in movimentos_validos:
        tabuleiro_simulado = list(tabuleiro)
        tabuleiro_simulado[movimento] = jogador_ia
        
        if verificar_vitoria(tabuleiro_simulado, jogador_ia):
            return movimento
        
    # Heurística - Vitória imediata do Humano (para bloquear)
    for movimento in movimentos_validos:
        tabuleiro_simulado = list(tabuleiro)
        tabuleiro_simulado[movimento] = jogador_humano
        
        if verificar_vitoria(tabuleiro_simulado, jogador_humano):
            return movimento
    
    # Fila FIFO para a BFS
    fila = collections.deque()
    
    # Adiciona os estados iniciais à fila (camada 1 da árvore)
    for movimento in movimentos_validos:
        novo_estado = list(tabuleiro)
        novo_estado[movimento] = jogador_ia
        fila.append((novo_estado, jogador_humano, movimento))
        
    numiteracoes = 0
    
    # Loop: explora camadas enquanto houver estados na fila (ela não está vazia)
    while fila and numiteracoes < 362880: 
        numiteracoes += 1
        
        # Remove o estado mais antigo da fila
        estado_atual, vez_de_quem, primeira_jogada = fila.popleft()
        
        # Verifica se esse caminho leva a vitória da IA
        if verificar_vitoria(estado_atual, jogador_ia):
            return primeira_jogada
        
        if tabuleiro_cheio(estado_atual):
            continue
    
        prox_jogador = 'X' if vez_de_quem == 'O' else 'O'
        
        # Expande o nó atual gerando filhos (ou seja, os próximos estados possíveis)
        for i in range(9):
            if estado_atual[i] == ' ':
                prox_estado = list(estado_atual)
                prox_estado[i] = vez_de_quem
                # Adiciona os filhos no final da fila para que sejam visitados posteriormente
                fila.append((prox_estado, prox_jogador, primeira_jogada))
        
    # Se não encontrou uma jogada vencedora, retorna um movimento aleatório válido (empate)
    return random.choice(movimentos_validos)

# ------------------------------------------------------------------------------
# LOOP DO JOGO + INTERFACE (terminal)
# ------------------------------------------------------------------------------
def jogo():
    tabuleiro = inicializar_tabuleiro()
    gameover = False
    print ("Jogo da velha com IA usando BFS!")
    print ("Você é 'X' e a IA é 'O'.")
    print("Para jogar, insira um número de 0 a 8 correspondente à posição no tabuleiro:")
    print(" 0 | 1 | 2 ")
    print(" 3 | 4 | 5 ")
    print(" 6 | 7 | 8 ")
    
    while not gameover:
        print ("Sua vez")
        imprimir_tabuleiro(tabuleiro)
        jogada_valida = False
        
        while not jogada_valida:
            
            try:
                escolha = int(input("Escolha sua jogada (0-8): "))
                
                if fazer_jogada(tabuleiro, escolha, 'X'):
                    jogada_valida = True
                    
                else:
                    print("Jogada inválida. Tente novamente.")
                    
            except ValueError:
                print("Entrada inválida. Insira um número de 0 a 8.")
    
        if verificar_vitoria(tabuleiro, 'X'):
            imprimir_tabuleiro(tabuleiro)
            print("Você venceu!")
            break
        
        if tabuleiro_cheio(tabuleiro):
            imprimir_tabuleiro(tabuleiro)
            print("Empate!")
            break
        
        print ("Vez da IA")
        tempoinicio = time.time()
        jogada_ia = bfs_melhor_jogada(tabuleiro, 'O')
        tempofim = time.time()
        
        print(f"IA jogou na posição {jogada_ia} (Tempo: {tempofim - tempoinicio:.6f}s)")
        
        fazer_jogada(tabuleiro, jogada_ia, 'O')
        
        if verificar_vitoria(tabuleiro, 'O'):
            imprimir_tabuleiro(tabuleiro)
            print("A IA venceu!")
            break
        
        if tabuleiro_cheio(tabuleiro):
            imprimir_tabuleiro(tabuleiro)
            print("Empate!")
            break

if __name__ == "__main__":
    jogo()