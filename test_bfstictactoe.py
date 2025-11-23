import pytest
import bfstictactoe as bfs

def test_inicializar_tabuleiro():
    tabuleiro = bfs.inicializar_tabuleiro()
    assert tabuleiro == [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
    assert len(tabuleiro) == 9

def test_fazer_jogada_valida():
    tabuleiro = bfs.inicializar_tabuleiro()
    assert bfs.fazer_jogada(tabuleiro, 0, 'X') == True
    assert tabuleiro[0] == 'X'

def test_fazer_jogada_invalida():
    tabuleiro = bfs.inicializar_tabuleiro()
    bfs.fazer_jogada(tabuleiro, 0, 'X')
    assert bfs.fazer_jogada(tabuleiro, 0, 'O') == False  
    assert bfs.fazer_jogada(tabuleiro, 9, 'O') == False 
    assert bfs.fazer_jogada(tabuleiro, -1, 'O') == False
    
def test_imprimir_tabuleiro(capsys):
    t = bfs.inicializar_tabuleiro()
    bfs.imprimir_tabuleiro(t)
    captured = capsys.readouterr()
    assert "--+---+--" in captured.out 
    assert "|" in captured.out

def test_verificar_vitoria_completo():
    combinacoes_vitoria = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8), 
        (0, 3, 6), (1, 4, 7), (2, 5, 8), 
        (0, 4, 8), (2, 4, 6)             
    ]

    for jogador in ['X', 'O']:
        adversario = 'O' if jogador == 'X' else 'X'
        
        for a, b, c in combinacoes_vitoria:
            tabuleiro = bfs.inicializar_tabuleiro()
            tabuleiro[a] = jogador
            tabuleiro[b] = jogador
            tabuleiro[c] = jogador
            
            mensagem_erro = f"Falhou: {jogador} deveria ganhar na pos {a},{b},{c}"
            assert bfs.verificar_vitoria(tabuleiro, jogador) is True, mensagem_erro 
            assert bfs.verificar_vitoria(tabuleiro, adversario) is False

def test_ia_etapa_1_vitoria_imediata():
    # Cenário: IA tem duas peças. Se jogar na posição certa, vence.
    t = bfs.inicializar_tabuleiro()
    t[0] = 'O'; t[1] = 'O'
    
    # A IA deve perceber que jogar na posição 2 garante a vitória AGORA.
    assert bfs.bfs_melhor_jogada(t, 'O') == 2

def test_ia_etapa_2_bloqueio():
    # Cenário: Jogador humano tem duas peças. IA deve bloquear.
    t = bfs.inicializar_tabuleiro()
    t[0] = 'X'; t[1] = 'X'
    
    # A IA deve jogar na posição 2 para salvar o jogo.
    assert bfs.bfs_melhor_jogada(t, 'O') == 2

def test_ia_etapa_3_bfs_futuro():
    # Cenário: Nenhum jogador pode vencer imediatamente. 
    t = ['X', ' ', 'X', 
         ' ', 'O', ' ', 
         'O', 'X', ' ']
    
    jogada = bfs.bfs_melhor_jogada(t, 'O')
    assert jogada in [1, 3, 5, 8] 
    assert jogada is not None

def test_ia_tabuleiro_cheio_entrada():
    t = ['X', 'O', 'X', 
         'X', 'O', 'O', 
         'O', 'X', 'X'] 
    assert bfs.bfs_melhor_jogada(t, 'O') is None
    
def test_ia_jogada_aleatoria():
    # Cenário: Tabuleiro vazio. A BFS não vai achar vitória imediata.
    t = bfs.inicializar_tabuleiro()
    jogada = bfs.bfs_melhor_jogada(t, 'X')
    assert jogada is not None
    assert 0 <= jogada <= 8