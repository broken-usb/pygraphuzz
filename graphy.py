import matplotlib.pyplot as plt
import numpy as np
import fuzzy_logic as fuzzy

# Responsável por desenhar os gráficos explicativos
# - Mostra funções de pertinência das entradas
# - Mostra a agregação e o resultado da defuzzificação

def plotar_graficos_reais(duracao_val, dificuldade_val):
    x_duracao = np.linspace(0, 24, 500)
    x_dificuldade = np.linspace(0, 10, 500)
    x_preco = np.linspace(0, 1000, 500)

    # Calculamos a ativação usando as funções do módulo fuzzy
    graus_dur = fuzzy.calcular_graus_duracao(duracao_val)
    graus_dif = fuzzy.calcular_graus_dificuldade(dificuldade_val)
    regras = fuzzy.calcular_regras(graus_dur, graus_dif)
    valor_final = fuzzy.defuzzificar(regras)

    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 10))

    # Funções de pertinência para a duração (curto/médio/longo)
    y_curto = [fuzzy.pertinencia_triangular(x, 0, 0, 12) for x in x_duracao]
    y_medio = [fuzzy.pertinencia_triangular(x, 0, 12, 24) for x in x_duracao]
    y_longo = [fuzzy.pertinencia_triangular(x, 12, 24, 24) for x in x_duracao]

    ax0.plot(x_duracao, y_curto, 'b', linewidth=1.5, label='Curto')
    ax0.plot(x_duracao, y_medio, 'g', linewidth=1.5, label='Médio')
    ax0.plot(x_duracao, y_longo, 'r', linewidth=1.5, label='Longo')
    
    ax0.axvline(x=duracao_val, color='k', linestyle='--', linewidth=2, label=f'Entrada: {duracao_val}h')
    ax0.set_title('Entrada 1: Duração do Serviço (0-24h)')
    ax0.legend()

    # Funções de pertinência para a dificuldade (fácil/média/difícil)
    y_facil = [fuzzy.pertinencia_triangular(x, 0, 0, 5) for x in x_dificuldade]
    y_media = [fuzzy.pertinencia_triangular(x, 0, 5, 10) for x in x_dificuldade]
    y_dificil = [fuzzy.pertinencia_triangular(x, 5, 10, 10) for x in x_dificuldade]

    ax1.plot(x_dificuldade, y_facil, 'b', linewidth=1.5, label='Fácil')
    ax1.plot(x_dificuldade, y_media, 'g', linewidth=1.5, label='Média')
    ax1.plot(x_dificuldade, y_dificil, 'r', linewidth=1.5, label='Difícil')
    
    ax1.axvline(x=dificuldade_val, color='k', linestyle='--', linewidth=2, label=f'Entrada: {dificuldade_val}')
    ax1.set_title('Entrada 2: Nível de Dificuldade')
    ax1.legend()

    # Funções de pertinência para o preço (saída)
    y_barato = [fuzzy.pertinencia_triangular(x, 0, 0, 500) for x in x_preco]
    y_justo = [fuzzy.pertinencia_triangular(x, 0, 500, 1000) for x in x_preco]
    y_caro = [fuzzy.pertinencia_triangular(x, 500, 1000, 1000) for x in x_preco]

    ax2.plot(x_preco, y_barato, 'b--', linewidth=0.5)
    ax2.plot(x_preco, y_justo, 'g--', linewidth=0.5)
    ax2.plot(x_preco, y_caro, 'r--', linewidth=0.5)

    # Aplica truncamento (clipping) pelas ativações das regras e agrega
    ativacao_b = np.fmin(regras['barato'], y_barato)
    ativacao_j = np.fmin(regras['justo'], y_justo)
    ativacao_c = np.fmin(regras['caro'], y_caro)
    agregado = np.fmax(ativacao_b, np.fmax(ativacao_j, ativacao_c))
    zeros = np.zeros(500)

    ax2.fill_between(x_preco, zeros, agregado, facecolor='orange', alpha=0.7)
    ax2.axvline(x=valor_final, color='k', linestyle='-', linewidth=3, label=f'Resultado: R$ {valor_final:.2f}')
    ax2.set_title('Saída: Valor do Serviço')
    ax2.legend()

    plt.tight_layout()
    plt.show()

zeros = np.zeros(500)

if __name__ == "__main__":
    # Valores utilizados para teste
    plotar_graficos_reais(2.5, 8.0)