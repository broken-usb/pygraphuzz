def pertinencia_triangular(x, a, b, c):
    if x == b: return 1.0
    if x <= a or x >= c: return 0.0
    if a < x < b: return (x - a) / (b - a)
    if b < x < c: return (c - x) / (c - b)
    return 0.0

def calcular_graus_duracao(tempo):
    """
    Nova escala de Tempo (0 a 48h) com 4 conjuntos assimétricos.
    """
    graus = {}
    
    # 1. Curto: < 0 até 8 (Pico em 0) - Foca na faixa "0 a 6"
    if tempo <= 0:
        graus['curto'] = 1.0
    else:
        graus['curto'] = pertinencia_triangular(tempo, 0, 0, 8)
    
    # 2. Levemente Longo: 6 até 14 (Pico em 10) - Foca na faixa "6 a 12"
    graus['levemente_longo'] = pertinencia_triangular(tempo, 6, 10, 14)
    
    # 3. Longo: 12 até 24 (Pico em 18) - Foca na faixa "10 a 20"
    graus['longo'] = pertinencia_triangular(tempo, 12, 18, 24)

    # 4. Muito Longo: 20 até >40 (Trapezóide a partir de 20)
    if tempo >= 40:
        graus['muito_longo'] = 1.0
    else:
        graus['muito_longo'] = pertinencia_triangular(tempo, 20, 40, 40)
    
    return graus

def calcular_graus_dificuldade(nivel):
    # Mantivemos a dificuldade igual (0-10)
    graus = {}
    if nivel <= 0: graus['facil'] = 1.0
    else: graus['facil'] = pertinencia_triangular(nivel, 0, 0, 5)
    
    graus['media'] = pertinencia_triangular(nivel, 0, 5, 10)
    
    if nivel >= 10: graus['dificil'] = 1.0
    else: graus['dificil'] = pertinencia_triangular(nivel, 5, 10, 10)
    
    return graus

def calcular_regras(graus_dur, graus_dif):
    """
    Matriz de 12 Regras (4 Tempos x 3 Dificuldades)
    """
    # Inicializa saídas
    grau_barato = 0.0
    grau_justo = 0.0
    grau_caro = 0.0
    grau_muito_caro = 0.0
    
    # --- REGRAS PARA BARATO ---
    # Curto + Fácil / Curto + Média / Levemente + Fácil
    r1 = min(graus_dur['curto'], graus_dif['facil'])
    r2 = min(graus_dur['curto'], graus_dif['media'])
    r3 = min(graus_dur['levemente_longo'], graus_dif['facil'])
    grau_barato = max(r1, r2, r3)

    # --- REGRAS PARA JUSTO ---
    # Curto + Difícil / Levemente + Média / Longo + Fácil
    r4 = min(graus_dur['curto'], graus_dif['dificil'])
    r5 = min(graus_dur['levemente_longo'], graus_dif['media'])
    r6 = min(graus_dur['levemente_longo'], graus_dif['dificil']) # Adicionei aqui
    r7 = min(graus_dur['longo'], graus_dif['facil'])
    grau_justo = max(r4, r5, r6, r7)

    # --- REGRAS PARA CARO ---
    # Longo + Média / Longo + Difícil / M. Longo + Fácil
    r8 = min(graus_dur['longo'], graus_dif['media'])
    r9 = min(graus_dur['longo'], graus_dif['dificil'])
    r10 = min(graus_dur['muito_longo'], graus_dif['facil'])
    r11 = min(graus_dur['muito_longo'], graus_dif['media'])
    grau_caro = max(r8, r9, r10, r11)

    # --- REGRAS PARA MUITO CARO ---
    # Muito Longo + Difícil
    r12 = min(graus_dur['muito_longo'], graus_dif['dificil'])
    grau_muito_caro = r12
    
    return {
        'barato': grau_barato,
        'justo': grau_justo,
        'caro': grau_caro,
        'muito_caro': grau_muito_caro
    }

def defuzzificar(resultados_regras):
    divida = 0.0
    divisor = 0.0
    passo = 20 # Passo maior pois o universo aumentou
    
    # Universo de Preço agora vai até 2000
    for x in range(0, 2001, passo):
        # Definição dos triângulos de saída
        pert_barato = pertinencia_triangular(x, 0, 0, 600)
        pert_justo  = pertinencia_triangular(x, 400, 800, 1200)
        pert_caro   = pertinencia_triangular(x, 1000, 1400, 1800)
        pert_mcaro  = pertinencia_triangular(x, 1600, 2000, 2000)
        
        # Corte (Mamdani)
        atv_barato = min(pert_barato, resultados_regras['barato'])
        atv_justo  = min(pert_justo, resultados_regras['justo'])
        atv_caro   = min(pert_caro, resultados_regras['caro'])
        atv_mcaro  = min(pert_mcaro, resultados_regras['muito_caro'])
        
        # Agregação
        grau_final = max(atv_barato, atv_justo, atv_caro, atv_mcaro)
        
        divida += x * grau_final
        divisor += grau_final
        
    if divisor == 0: return 0.0
    return divida / divisor