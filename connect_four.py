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


def dentro_do_tabuleiro(linha, coluna):
    return 0 <= linha < LINHAS and 0 <= coluna < COLUNAS


def verificar_vitoria(tabuleiro, jogador):
    """Procura 4 fichas seguidas do jogador em qualquer direção.

    Para cada casa e cada direção de DIRECOES, monta as 4 posições
    a partir daquela casa. Se todas estiverem dentro do tabuleiro e
    pertencerem ao jogador, há vitória.

    Retorna a lista com as 4 posições (linha, coluna) vencedoras,
    ou uma lista vazia se não houver vitória.
    """
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            for passo_l, passo_c in DIRECOES:
                posicoes = [(linha + i * passo_l, coluna + i * passo_c)
                            for i in range(SEQUENCIA)]
                if all(dentro_do_tabuleiro(l, c) and tabuleiro[l][c] == jogador
                       for l, c in posicoes):
                    return posicoes
    return []


def tabuleiro_cheio(tabuleiro):
    """Empate: todas as colunas estão cheias."""
    return all(coluna_cheia(tabuleiro, c) for c in range(COLUNAS))


def outro_jogador(jogador):
    return 2 if jogador == 1 else 1


# ============================== Interface gráfica ==============================

def centro_da_casa(linha, coluna):
    """Converte (linha, coluna) da matriz no centro da casa, em pixels."""
    x = coluna * CELULA + CELULA // 2
    y = TOPO + linha * CELULA + CELULA // 2
    return x, y


def desenhar_tabuleiro(window, tabuleiro, vencedoras=()):
    """Redesenha o tabuleiro inteiro a partir da matriz.

    vencedoras: posições que recebem um anel branco de destaque.
    """
    grafico = window['-TABULEIRO-']
    grafico.erase()

    # Números das colunas na faixa superior
    for coluna in range(COLUNAS):
        x = coluna * CELULA + CELULA // 2
        grafico.draw_text(str(coluna + 1), (x, TOPO // 2),
                          color='white', font=('Helvetica', 14, 'bold'))

    # Fundo azul do tabuleiro
    grafico.draw_rectangle((0, TOPO), (LARGURA, ALTURA),
                           fill_color=COR_TABULEIRO, line_color=COR_TABULEIRO)

    # Casas: vazias ou com a cor do jogador
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            valor = tabuleiro[linha][coluna]
            cor = COR_VAZIO if valor == VAZIO else CORES_JOGADOR[valor]
            grafico.draw_circle(centro_da_casa(linha, coluna), RAIO,
                                fill_color=cor, line_color=COR_BORDA, line_width=2)

    # Destaque das 4 fichas vencedoras
    for linha, coluna in vencedoras:
        grafico.draw_circle(centro_da_casa(linha, coluna), RAIO - 7,
                            line_color=COR_DESTAQUE, line_width=5)


def mostrar_status(window, texto, cor):
    window['-STATUS-'].update(texto, text_color=cor)


def mostrar_vez(window, jogador):
    mostrar_status(window, f'Vez do Jogador {jogador} ({NOMES_JOGADOR[jogador]})',
                   CORES_JOGADOR[jogador])


def mostrar_placar(window, placar):
    window['-PLACAR-'].update(
        f'Placar  |  {NOMES_JOGADOR[1]}: {placar[1]}   '
        f'{NOMES_JOGADOR[2]}: {placar[2]}   Empates: {placar["empates"]}'
    )


def novo_estado(quem_comeca=1):
    """Agrupa tudo que muda durante uma partida em um dicionário."""
    return {
        'tabuleiro': criar_tabuleiro(),
        'jogador': quem_comeca,
        'quem_comeca': quem_comeca,
        'ativo': True,     # False depois de vitória ou empate
    }


def jogar(window, estado, placar, coluna):
    """Processa uma jogada na coluna escolhida."""
    if not estado['ativo']:
        return

    tabuleiro = estado['tabuleiro']
    jogador = estado['jogador']

    # Validação de coluna cheia: avisa e NÃO passa a vez
    if coluna_cheia(tabuleiro, coluna):
        mostrar_status(window, f'Coluna {coluna + 1} cheia! Escolha outra.',
                       CORES_JOGADOR[jogador])
        return

    inserir_ficha(tabuleiro, coluna, jogador)
    vencedoras = verificar_vitoria(tabuleiro, jogador)
    desenhar_tabuleiro(window, tabuleiro, vencedoras)

    if vencedoras:
        estado['ativo'] = False
        placar[jogador] += 1
        mensagem = f'Jogador {jogador} ({NOMES_JOGADOR[jogador]}) venceu!'
        mostrar_status(window, mensagem, CORES_JOGADOR[jogador])
        mostrar_placar(window, placar)
        window.refresh()   # garante que o tabuleiro aparece antes do popup
        sg.popup(mensagem, 'Clique em "Reiniciar Jogo" para jogar de novo.',
                 title='Fim de jogo', keep_on_top=True)
    elif tabuleiro_cheio(tabuleiro):
        estado['ativo'] = False
        placar['empates'] += 1
        mostrar_status(window, 'Empate! O tabuleiro está cheio.', COR_EMPATE)
        mostrar_placar(window, placar)
        window.refresh()
        sg.popup('Empate! Ninguém alinhou 4 fichas.',
                 title='Fim de jogo', keep_on_top=True)
    else:
        estado['jogador'] = outro_jogador(jogador)
        mostrar_vez(window, estado['jogador'])


def coluna_do_evento(event, values):
    """Descobre a coluna escolhida a partir de um clique ou tecla.

    Retorna o índice da coluna (0 a 6) ou None se o evento não for jogada.
    """
    if event == '-TABULEIRO-':
        x, _ = values['-TABULEIRO-']
        if x is None:
            return None
        return min(max(int(x) // CELULA, 0), COLUNAS - 1)

    # Teclas 1 a 7 (o FreeSimpleGUI devolve o caractere como evento)
    if isinstance(event, str) and len(event) >= 1 and event[0] in '1234567':
        if len(event) == 1 or event[1] == ':':
            return int(event[0]) - 1

    return None


def criar_janela():
    sg.theme('Black')

    layout = [
        [sg.Text('CONNECT FOUR', font=('Helvetica', 22, 'bold'),
                 justification='center', expand_x=True)],
        [sg.Text('', key='-STATUS-', font=('Helvetica', 14, 'bold'),
                 justification='center', expand_x=True)],
        [sg.Graph(canvas_size=(LARGURA, ALTURA),
                  graph_bottom_left=(0, ALTURA),   # eixo y cresce para baixo,
                  graph_top_right=(LARGURA, 0),    # igual aos índices da matriz
                  background_color=COR_FUNDO,
                  key='-TABULEIRO-', enable_events=True)],
        [sg.Text('', key='-PLACAR-', font=('Helvetica', 12),
                 justification='center', expand_x=True)],
        [sg.Button('Reiniciar Jogo', key='-REINICIAR-', size=(14, 1)),
         sg.Button('Zerar Placar', key='-ZERAR-', size=(14, 1)),
         sg.Button('Sair', key='-SAIR-', size=(10, 1))],
        [sg.Text('Clique na coluna ou use as teclas 1 a 7',
                 font=('Helvetica', 10), justification='center', expand_x=True)],
    ]

    return sg.Window('INE5201 - Connect Four', layout, finalize=True,
                     element_justification='center',
                     return_keyboard_events=True)


# ============================== Programa principal ==============================

def main():
    window = criar_janela()
    placar = {1: 0, 2: 0, 'empates': 0}
    estado = novo_estado(quem_comeca=1)

    desenhar_tabuleiro(window, estado['tabuleiro'])
    mostrar_vez(window, estado['jogador'])
    mostrar_placar(window, placar)

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, '-SAIR-'):
            break

        if event == '-REINICIAR-':
            # Quem começa alterna a cada partida, para ser justo
            estado = novo_estado(outro_jogador(estado['quem_comeca']))
            desenhar_tabuleiro(window, estado['tabuleiro'])
            mostrar_vez(window, estado['jogador'])
            continue

        if event == '-ZERAR-':
            placar = {1: 0, 2: 0, 'empates': 0}
            mostrar_placar(window, placar)
            continue

        coluna = coluna_do_evento(event, values)
        if coluna is not None:
            jogar(window, estado, placar, coluna)

    window.close()


if __name__ == '__main__':
    main()
