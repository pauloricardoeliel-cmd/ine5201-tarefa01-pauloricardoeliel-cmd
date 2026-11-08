"""
Connect Four (Quatro em Linha) com interface gráfica
INE5201 - Introdução à Ciência da Computação com Python - UFSC
Tarefa 01

Dupla:
    Matheus da Silva Farani (24202994)
    Paulo Ricardo Eliel Mendes Peres dos Santos (24100434)

Como jogar:
    Clique em qualquer ponto de uma coluna (ou use as teclas 1 a 7)
    para soltar uma ficha. Vence quem alinhar 4 fichas da mesma cor
    na horizontal, vertical ou diagonal.
"""

import FreeSimpleGUI as sg

# ============================== Constantes ==============================

LINHAS = 6
COLUNAS = 7
VAZIO = 0          # valor de uma casa sem ficha na matriz
SEQUENCIA = 4      # quantas fichas alinhadas são necessárias para vencer

# Dimensões do desenho (em pixels)
CELULA = 80                     # lado de cada casa
RAIO = 32                       # raio de cada ficha
TOPO = 40                       # faixa acima do tabuleiro com os números das colunas
LARGURA = COLUNAS * CELULA
ALTURA = TOPO + LINHAS * CELULA

# Cores
COR_FUNDO = '#000000'
COR_TABULEIRO = '#1F4FBF'
COR_BORDA = '#123A8C'
COR_VAZIO = '#E8EEF7'
COR_DESTAQUE = '#FFFFFF'        # anel em volta das fichas vencedoras
COR_EMPATE = '#F4A261'

CORES_JOGADOR = {1: '#E63946', 2: '#FFD23F'}
NOMES_JOGADOR = {1: 'Vermelho', 2: 'Amarelo'}

# Direções verificadas na busca de 4 em linha: (passo na linha, passo na coluna)
DIRECOES = [
    (0, 1),    # horizontal  →
    (1, 0),    # vertical    ↓
    (1, 1),    # diagonal    ↘
    (1, -1),   # diagonal    ↙
]


# ============================== Lógica do jogo ==============================

def criar_tabuleiro():
    """Retorna uma matriz LINHAS x COLUNAS preenchida com VAZIO.

    A linha 0 é a do topo e a linha LINHAS-1 é a do fundo.
    Cada linha é criada separadamente; [[0]*7]*6 faria as 6 linhas
    apontarem para a MESMA lista, e uma jogada apareceria em todas.
    """
    return [[VAZIO] * COLUNAS for _ in range(LINHAS)]


def coluna_cheia(tabuleiro, coluna):
    """Uma coluna está cheia quando a casa do topo já tem ficha."""
    return tabuleiro[0][coluna] != VAZIO


def inserir_ficha(tabuleiro, coluna, jogador):
    """Solta a ficha do jogador na coluna, aplicando a gravidade.

    Percorre a coluna de baixo para cima e ocupa a primeira casa vazia.
    Retorna a linha onde a ficha parou, ou -1 se a coluna estiver cheia.
    """
    for linha in range(LINHAS - 1, -1, -1):
        if tabuleiro[linha][coluna] == VAZIO:
            tabuleiro[linha][coluna] = jogador
            return linha
    return -1

