import matplotlib.pyplot as plt
import numpy as np
import fuzzy_logic as fuzzy

def plotar_graficos_reais(duracao_val, dificuldade_val):
    # Plota três gráficos explicativos: duração, dificuldade e saída (preço).
    # Os arrays X servem para desenhar as funções de pertinência suavemente.
    x_duracao = np.linspace(0, 42, 500)
    x_dificuldade = np.linspace(0, 10, 500)
    x_preco = np.linspace(0, 2000, 500)

    graus_dur = fuzzy.calcular_graus_duracao(duracao_val)
    graus_dif = fuzzy.calcular_graus_dificuldade(dificuldade_val)
    regras = fuzzy.calcular_regras(graus_dur, graus_dif)
    valor_final = fuzzy.defuzzificar(regras)

    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(10, 12))
    plt.subplots_adjust(hspace=0.4) 

    # TEMPO
    # Curvas de pertinência para as etiquetas de duração (visualização).
    y_curto = [fuzzy.pertinencia_trapezoidal(x, -100, 0, 0, 8) for x in x_duracao]
    y_leve = [fuzzy.pertinencia_triangular(x, 6, 10, 14) for x in x_duracao]
    y_longo = [fuzzy.pertinencia_triangular(x, 12, 18, 24) for x in x_duracao]
    y_mlongo = [fuzzy.pertinencia_trapezoidal(x, 20, 40, 100, 100) for x in x_duracao]

    ax0.plot(x_duracao, y_curto, 'b', label='Curto')
    ax0.plot(x_duracao, y_leve, 'c', label='Leve. Longo')
    ax0.plot(x_duracao, y_longo, 'g', label='Longo')
    ax0.plot(x_duracao, y_mlongo, 'r', label='Muito Longo')
    ax0.axvline(x=duracao_val, color='k', linestyle='--', linewidth=2, label=f'Entrada: {duracao_val}h')

    # Marca os pontos de ativação para a entrada atual
    cores_map_dur = {'curto': 'b', 'levemente_longo': 'c', 'longo': 'g', 'muito_longo': 'r'}
    for termo, valor in graus_dur.items():
        if valor > 0:
            ax0.plot(duracao_val, valor, 'o', color=cores_map_dur[termo], zorder=10)
            ax0.hlines(valor, 0, duracao_val, colors=cores_map_dur[termo], linestyles='dotted')
            ax0.text(duracao_val + 0.5, valor, f"{valor:.2f}", color=cores_map_dur[termo], fontweight='bold')

    ax0.set_title('Entrada 1: Duração (0-42h)')
    ax0.legend(loc='upper right')

    # DIFICULDADE
    # Curvas para fácil/média/difícil
    y_facil = [fuzzy.pertinencia_trapezoidal(x, -10, 0, 0, 5) for x in x_dificuldade]
    y_media = [fuzzy.pertinencia_triangular(x, 0, 5, 10) for x in x_dificuldade]
    y_dificil = [fuzzy.pertinencia_trapezoidal(x, 5, 10, 20, 20) for x in x_dificuldade]

    ax1.plot(x_dificuldade, y_facil, 'b', label='Fácil')
    ax1.plot(x_dificuldade, y_media, 'g', label='Média')
    ax1.plot(x_dificuldade, y_dificil, 'r', label='Difícil')
    ax1.axvline(x=dificuldade_val, color='k', linestyle='--', label=f'Entrada: {dificuldade_val}')

    # Pontos de ativação para dificuldade
    cores_map_dif = {'facil': 'b', 'media': 'g', 'dificil': 'r'}
    for termo, valor in graus_dif.items():
        if valor > 0:
            ax1.plot(dificuldade_val, valor, 'o', color=cores_map_dif[termo])
            ax1.hlines(valor, 0, dificuldade_val, colors=cores_map_dif[termo], linestyles='dotted')
            ax1.text(dificuldade_val + 0.2, valor, f"{valor:.2f}", color=cores_map_dif[termo], fontweight='bold')

    ax1.set_title('Entrada 2: Dificuldade')
    ax1.legend(loc='upper right')

    # SAIDA
    # Curvas de saída (barato/justo/caro/muito caro) e área ativada
    y_barato = [fuzzy.pertinencia_trapezoidal(x, -500, 0, 0, 600) for x in x_preco]
    y_justo  = [fuzzy.pertinencia_triangular(x, 400, 800, 1200) for x in x_preco]
    y_caro   = [fuzzy.pertinencia_triangular(x, 1000, 1400, 1800) for x in x_preco]
    y_mcaro  = [fuzzy.pertinencia_trapezoidal(x, 1600, 2000, 3000, 3000) for x in x_preco]

    ax2.plot(x_preco, y_barato, 'b:', alpha=0.5)
    ax2.plot(x_preco, y_justo, 'g:', alpha=0.5)
    ax2.plot(x_preco, y_caro, 'orange', linestyle=':', alpha=0.5)
    ax2.plot(x_preco, y_mcaro, 'r:', alpha=0.5)

    # Aplica os níveis de ativação das regras (fatiamento / clipping)
    atv_b = np.fmin(regras['barato'], y_barato)
    atv_j = np.fmin(regras['justo'], y_justo)
    atv_c = np.fmin(regras['caro'], y_caro)
    atv_mc = np.fmin(regras['muito_caro'], y_mcaro)

    agregado = np.fmax(atv_b, np.fmax(atv_j, np.fmax(atv_c, atv_mc)))
    zeros = np.zeros(500)

    # Preenche as áreas ativadas para visualização
    ax2.fill_between(x_preco, zeros, atv_b, facecolor='blue', alpha=0.3, label='Barato')
    ax2.fill_between(x_preco, zeros, atv_j, facecolor='green', alpha=0.3, label='Justo')
    ax2.fill_between(x_preco, zeros, atv_c, facecolor='orange', alpha=0.3, label='Caro')
    ax2.fill_between(x_preco, zeros, atv_mc, facecolor='red', alpha=0.3, label='Muito Caro')

    ax2.plot(x_preco, agregado, color='k', linewidth=2)
    ax2.axvline(x=valor_final, color='k', linewidth=3)
    ax2.text(valor_final + 50, 0.5, f"R$ {valor_final:.2f}", fontweight='bold', fontsize=12)

    ax2.set_title('Saída: Preço (0 a 2000)')
    ax2.legend(loc='upper right')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plotar_graficos_reais(41.0, 8.0)