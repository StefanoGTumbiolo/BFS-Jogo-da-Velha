# ------------------------------------------------------------------------------
# LÓGICA GERAL
# ------------------------------------------------------------------------------

# [ ] CLASSE OU ESTRUTURA DO JOGO
#     Deve conter o estado do tabuleiro, como uma lista simples de 9 strings aonde cada posição pode ser ' ', 'X' ou 'O'.

# [ ] FUNÇÃO: inicializar_tabuleiro()
#     - Retorna uma lista [' ', ' ', ..., ' '] de 9 posições.

# [ ] FUNÇÃO: fazer_jogada(tabuleiro, posicao, jogador)
#     - Verifica se a posição é válida (se estiver vazia e dentro do range).
#     - Insere 'X' ou 'O' na posição.
#     - Retorna True se funcionou, False se inválido.

# [ ] FUNÇÃO: verificar_vitoria(tabuleiro, jogador)
#     - Verifica as 3 linhas, 3 colunas e 2 diagonais.
#     - Retorna True se o jogador venceu, ou seja, se há 3 símbolos iguais em linha, coluna ou diagonal.

# [ ] FUNÇÃO: tabuleiro_cheio(tabuleiro)
#     - Verifica se não há mais espaços vazios (vai acontecer se o jogo terminou em empate).

# [ ] FUNÇÃO: obter_movimentos_validos(tabuleiro)
#     - Retorna uma lista de índices (0-8) que estão vazios.
#     - Vai ser usada pela IA para saber onde pode jogar.

# [ ] FUNÇÃO: imprimir_tabuleiro(tabuleiro)
#     - Mostra o estado atual do jogo no terminal durante a vez do jogador humano.

# ------------------------------------------------------------------------------
# USO DA BFS
# ------------------------------------------------------------------------------

# [ ] FUNÇÃO: bfs_melhor_jogada(jogo, jogador_ia)
#     Esta função deve ser o foco do projeto.
#
#     ETAPA 1: Vitória Imediata
#     - [ ] Loop que passa pelos movimentos possíveis.
#     - [ ] Simula jogada da IA. Se ganhar, RETORNAR essa jogada imediatamente.
#
#     ETAPA 2: Heurística de Bloqueio (Defesa)
#     - [ ] Loop que passa pelos movimentos possíveis.
#     - [ ] Simula jogada do HUMANO. Se humano ganharia, RETORNAR essa jogada (ou seja, a IA deve BLOQUEAR).
#
#     ETAPA 3: Algoritmo BFS (Busca em Largura)
#     - [ ] Criar Fila (queue = collections.deque()).
#     - [ ] Adicionar estados iniciais na fila: (estado_tabuleiro, vez_de_quem, primeira_jogada).
#     - [ ] Loop WHILE enquanto a fila não estiver vazia:
#           - Retirar elemento mais antigo.
#           - Gerar filhos (próximos movimentos possíveis).
#           - Verificar se filho é estado de vitória.
#           - Se vitória: RETORNAR a 'primeira_jogada' que iniciou esse caminho que leva à vitória.
#           - Se não: Adicionar filho ao final da fila para verificar os próximos níveis.
#
#     ETAPA 4: Caso de empate ou sem vitória possível
#     - [ ] Se BFS não achar nada (tudo leva a empate), jogar em posição aleatória.