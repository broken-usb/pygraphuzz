import matplotlib.pyplot as plt
import numpy as np
import fuzzy_logic as fuzzy

def plotar_graficos_reais(duracao_val, dificuldade_val):
    # Valores X para desenhar as curvas
    x_duracao = np.linspace(0, 24, 500)
    x_dificuldade = np.linspace(0, 10, 500)
    x_preco = np.linspace(0, 1000, 500)

    # Calcula graus, aplica regras e obtém o resultado
    graus_dur = fuzzy.calcular_graus_duracao(duracao_val)
    graus_dif = fuzzy.calcular_graus_dificuldade(dificuldade_val)
    regras = fuzzy.calcular_regras(graus_dur, graus_dif)
    valor_final = fuzzy.defuzzificar(regras)

    # Prepara a figura com 3 painéis (duração, dificuldade, saída)
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(10, 12))
    plt.subplots_adjust(hspace=0.4)

    # --- Gráfico 1: Duração ---
    y_curto = [fuzzy.pertinencia_triangular(x, 0, 0, 12) for x in x_duracao]
    y_medio = [fuzzy.pertinencia_triangular(x, 0, 12, 24) for x in x_duracao]
    y_longo = [fuzzy.pertinencia_triangular(x, 12, 24, 24) for x in x_duracao]

    ax0.plot(x_duracao, y_curto, 'b', linewidth=1.5, label='Curto')
    ax0.plot(x_duracao, y_medio, 'g', linewidth=1.5, label='Médio')
    ax0.plot(x_duracao, y_longo, 'r', linewidth=1.5, label='Longo')
    ax0.axvline(x=duracao_val, color='k', linestyle='--', linewidth=2, label=f'Entrada: {duracao_val}h')

    # Marca os pontos de ativação na entrada (pequenos círculos e valores)
    cores_map_dur = {'curto': 'b', 'medio': 'g', 'longo': 'r'}
    for termo, valor in graus_dur.items():
        if valor > 0:
            ax0.plot(duracao_val, valor, 'o', color=cores_map_dur[termo], zorder=10)
            ax0.hlines(valor, 0, duracao_val, colors=cores_map_dur[termo], linestyles='dotted')
            ax0.text(duracao_val + 0.5, valor, f"{valor:.2f}", color=cores_map_dur[termo], fontweight='bold')

    ax0.set_title('Entrada 1: Duração do Serviço (0-24h)')
    ax0.legend(loc='upper right')

    # --- Gráfico 2: Dificuldade ---
    y_facil = [fuzzy.pertinencia_triangular(x, 0, 0, 5) for x in x_dificuldade]
    y_media = [fuzzy.pertinencia_triangular(x, 0, 5, 10) for x in x_dificuldade]
    y_dificil = [fuzzy.pertinencia_triangular(x, 5, 10, 10) for x in x_dificuldade]

    ax1.plot(x_dificuldade, y_facil, 'b', linewidth=1.5, label='Fácil')
    ax1.plot(x_dificuldade, y_media, 'g', linewidth=1.5, label='Média')
    ax1.plot(x_dificuldade, y_dificil, 'r', linewidth=1.5, label='Difícil')
    ax1.axvline(x=dificuldade_val, color='k', linestyle='--', linewidth=2, label=f'Entrada: {dificuldade_val}')
    
    # Marca os pontos de ativação para a dificuldade
    cores_map_dif = {'facil': 'b', 'media': 'g', 'dificil': 'r'}
    for termo, valor in graus_dif.items():
        if valor > 0:
            ax1.plot(dificuldade_val, valor, 'o', color=cores_map_dif[termo], zorder=10)
            ax1.hlines(valor, 0, dificuldade_val, colors=cores_map_dif[termo], linestyles='dotted')
            ax1.text(dificuldade_val + 0.2, valor, f"{valor:.2f}", color=cores_map_dif[termo], fontweight='bold')

    ax1.set_title('Entrada 2: Nível de Dificuldade')
    ax1.legend(loc='upper right')

    # --- Gráfico 3: Saída ---
    # Linhas de referência para as funções de pertinência do preço
    y_barato = [fuzzy.pertinencia_triangular(x, 0, 0, 500) for x in x_preco]
    y_justo = [fuzzy.pertinencia_triangular(x, 0, 500, 1000) for x in x_preco]
    y_caro = [fuzzy.pertinencia_triangular(x, 500, 1000, 1000) for x in x_preco]

    ax2.plot(x_preco, y_barato, 'b:', linewidth=0.8, alpha=0.5)
    ax2.plot(x_preco, y_justo, 'g:', linewidth=0.8, alpha=0.5)
    ax2.plot(x_preco, y_caro, 'r:', linewidth=0.8, alpha=0.5)

    # Aplica a ativação (corta cada função pelo grau da regra)
    ativacao_b = np.fmin(regras['barato'], y_barato)
    ativacao_j = np.fmin(regras['justo'], y_justo)
    ativacao_c = np.fmin(regras['caro'], y_caro)
    
    # Agrega as áreas ativadas (contorno final)
    agregado = np.fmax(ativacao_b, np.fmax(ativacao_j, ativacao_c))
    zeros = np.zeros(500)

    # Pinta cada categoria com transparência para mostrar sobreposição
    ax2.fill_between(x_preco, zeros, ativacao_b, facecolor='blue', alpha=0.3, label='Barato')
    ax2.fill_between(x_preco, zeros, ativacao_j, facecolor='green', alpha=0.3, label='Justo')
    ax2.fill_between(x_preco, zeros, ativacao_c, facecolor='red', alpha=0.3, label='Caro')

    # Contorno agregado e linha do resultado (centroide)
    ax2.plot(x_preco, agregado, color='k', linewidth=2, label='Agregação')
    ax2.axvline(x=valor_final, color='k', linestyle='-', linewidth=3)
    ax2.text(valor_final + 10, 0.5, f"Centroide: R$ {valor_final:.2f}", fontweight='bold', fontsize=12)

    ax2.set_title('Saída: Áreas de Ativação e Resultado Final')
    ax2.legend(loc='upper right')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plotar_graficos_reais(3.0, 4.0)