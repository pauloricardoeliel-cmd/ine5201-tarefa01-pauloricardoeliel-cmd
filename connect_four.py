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

