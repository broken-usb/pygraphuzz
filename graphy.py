import matplotlib.pyplot as plt
import numpy as np
import fuzzy_logic as fuzzy

def plotar_graficos_reais(duracao_val, dificuldade_val, metodo='mamdani'):
    # Definindo os universos
    x_duracao = np.linspace(0, 24, 500)
    x_dificuldade = np.linspace(0, 10, 500)
    x_preco = np.linspace(0, 1000, 500)

    # 1. Cálculos do sistema Fuzzy
    graus_dur = fuzzy.calcular_graus_duracao(duracao_val)
    graus_dif = fuzzy.calcular_graus_dificuldade(dificuldade_val)
    regras = fuzzy.calcular_regras(graus_dur, graus_dif)
    
    # Passamos o método escolhido para o cálculo final
    valor_final = fuzzy.defuzzificar(regras, metodo=metodo)

    # 2. Configuração da Figura (Layout 2x2)
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    # --- GRÁFICO 1: DURAÇÃO ---
    ax0 = axs[0, 0]
    y_curto = [fuzzy.pertinencia_triangular(x, 0, 0, 12) for x in x_duracao]
    y_medio = [fuzzy.pertinencia_triangular(x, 0, 12, 24) for x in x_duracao]
    y_longo = [fuzzy.pertinencia_triangular(x, 12, 24, 24) for x in x_duracao]
    
    ax0.plot(x_duracao, y_curto, 'b', label='Curto')
    ax0.plot(x_duracao, y_medio, 'g', label='Médio')
    ax0.plot(x_duracao, y_longo, 'r', label='Longo')
    ax0.set_title(f'Entrada 1: Duração ({duracao_val}h)')
    ax0.axvline(x=duracao_val, color='k', linestyle='--', alpha=0.5)

    # Bolinhas de interseção
    cores_map = {'curto': 'b', 'medio': 'g', 'longo': 'r'}
    for nome, grau in graus_dur.items():
        if grau > 0:
            ax0.plot(duracao_val, grau, 'o', color=cores_map[nome])
            ax0.hlines(grau, 0, duracao_val, colors=cores_map[nome], linestyles='dotted')
            ax0.text(duracao_val + 0.5, grau, f"{grau:.2f}", fontsize=9, color=cores_map[nome], fontweight='bold')
    ax0.legend(loc='upper right', fontsize='small')

    # --- GRÁFICO 2: DIFICULDADE ---
    ax1 = axs[0, 1]
    y_facil = [fuzzy.pertinencia_triangular(x, 0, 0, 5) for x in x_dificuldade]
    y_media = [fuzzy.pertinencia_triangular(x, 0, 5, 10) for x in x_dificuldade]
    y_dificil = [fuzzy.pertinencia_triangular(x, 5, 10, 10) for x in x_dificuldade]

    ax1.plot(x_dificuldade, y_facil, 'b', label='Fácil')
    ax1.plot(x_dificuldade, y_media, 'g', label='Média')
    ax1.plot(x_dificuldade, y_dificil, 'r', label='Difícil')
    ax1.set_title(f'Entrada 2: Dificuldade ({dificuldade_val})')
    ax1.axvline(x=dificuldade_val, color='k', linestyle='--', alpha=0.5)

    cores_map_dif = {'facil': 'b', 'media': 'g', 'dificil': 'r'}
    for nome, grau in graus_dif.items():
        if grau > 0:
            ax1.plot(dificuldade_val, grau, 'o', color=cores_map_dif[nome])
            ax1.hlines(grau, 0, dificuldade_val, colors=cores_map_dif[nome], linestyles='dotted')
            ax1.text(dificuldade_val + 0.2, grau, f"{grau:.2f}", fontsize=9, color=cores_map_dif[nome], fontweight='bold')
    ax1.legend(loc='upper right', fontsize='small')

    # --- GRÁFICO 3: MÉTODO DE INFERÊNCIA ---
    ax2 = axs[1, 0]
    y_barato = np.array([fuzzy.pertinencia_triangular(x, 0, 0, 500) for x in x_preco])
    y_justo = np.array([fuzzy.pertinencia_triangular(x, 0, 500, 1000) for x in x_preco])
    y_caro = np.array([fuzzy.pertinencia_triangular(x, 500, 1000, 1000) for x in x_preco])

    ax2.plot(x_preco, y_barato, 'b', linewidth=1, alpha=0.3)
    ax2.plot(x_preco, y_justo, 'g', linewidth=1, alpha=0.3)
    ax2.plot(x_preco, y_caro, 'r', linewidth=1, alpha=0.3)
    
    # Lógica de Visualização Mamdani vs Larsen
    if metodo == 'minimo':
        ax2.set_title('Inferência: Corte (Mínimo)')
        # Calcula o corte
        ativacao_b = np.fmin(regras['barato'], y_barato)
        ativacao_j = np.fmin(regras['justo'], y_justo)
        ativacao_c = np.fmin(regras['caro'], y_caro)
        # Linhas de corte tracejadas
        if regras['barato'] > 0: ax2.hlines(regras['barato'], 0, 1000, colors='b', linestyles='dashed')
        if regras['justo'] > 0: ax2.hlines(regras['justo'], 0, 1000, colors='g', linestyles='dashed')
        if regras['caro'] > 0: ax2.hlines(regras['caro'], 0, 1000, colors='r', linestyles='dashed')
    else:
        ax2.set_title('Inferência: Escala (Produto)')
        # Calcula a escala (multiplicação)
        ativacao_b = y_barato * regras['barato']
        ativacao_j = y_justo * regras['justo']
        ativacao_c = y_caro * regras['caro']
        
    # Desenha as áreas resultantes de cada conjunto individualmente
    ax2.fill_between(x_preco, 0, ativacao_b, color='b', alpha=0.1)
    ax2.fill_between(x_preco, 0, ativacao_j, color='g', alpha=0.1)
    ax2.fill_between(x_preco, 0, ativacao_c, color='r', alpha=0.1)

    # --- GRÁFICO 4: AGREGAÇÃO FINAL ---
    ax3 = axs[1, 1]
    
    # Agrega tudo (MAX)
    agregado = np.fmax(ativacao_b, np.fmax(ativacao_j, ativacao_c))
    
    ax3.fill_between(x_preco, 0, agregado, facecolor='orange', alpha=0.6, label='Área Agregada')
    ax3.plot(x_preco, agregado, 'k', linewidth=1)
    
    ax3.axvline(x=valor_final, color='k', linestyle='-', linewidth=3, label='Centroide')
    ax3.text(valor_final + 10, 0.1, f"R$ {valor_final:.2f}", fontweight='bold')
    
    ax3.set_title('Resultado Final (Defuzzificação)')
    ax3.legend()

    plt.show()