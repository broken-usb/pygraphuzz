def pertinencia_triangular(x, a, b, c):
    # Grau de pertinencia triangular.
    # Retorna um valor entre 0 e 1 informando o quanto `x` pertence
    # ao conjunto descrito pelos pontos (a,b,c).
    
    # Pico
    if x == b:
        return 1.0
        
    # Fora
    if x <= a or x >= c:
        return 0.0
    
    # Subida
    if a < x < b:
        return (x - a) / (b - a)
    
    # Descida
    if b < x < c:
        return (c - x) / (c - b)
    
    return 0.0

def calcular_graus_duracao(tempo):
    graus = {}
    # Curto = 0 a 12
    if tempo <= 0:
        graus['curto'] = 1.0
    else:
        graus['curto'] = pertinencia_triangular(tempo, 0, 0, 12)
    
    # Médio = 0 a 12 a 24
    graus['medio'] = pertinencia_triangular(tempo, 0, 12, 24)
    
    # Longo = 12 a 24
    if tempo >= 24:
        graus['longo'] = 1.0
    else:
        graus['longo'] = pertinencia_triangular(tempo, 12, 24, 24)
    
    return graus

def calcular_graus_dificuldade(nivel):
    graus = {}
    # Calcula os graus de pertinência para o nível de dificuldade
    
    # Grafico do Facil (Trapezio)
    if nivel <= 0:
        graus['facil'] = 1.0
    else:
        graus['facil'] = pertinencia_triangular(nivel, 0, 0, 5)
    
    # Grafico do Medio (Triangulo)
    graus['media'] = pertinencia_triangular(nivel, 0, 5, 10)
    
    # Grafico do Dificil (Trapezio)
    if nivel >= 10:
        graus['dificil'] = 1.0
    else:
        graus['dificil'] = pertinencia_triangular(nivel, 5, 10, 10)
    
    return graus

def calcular_regras(graus_duracao, graus_dificuldade):
    grau_barato = 0.0
    grau_justo = 0.0
    grau_caro = 0.0
    
    # Regras que levam à saída 'barato'
    regra1 = min(graus_duracao['curto'], graus_dificuldade['facil'])
    regra2 = min(graus_duracao['curto'], graus_dificuldade['media'])
    regra3 = min(graus_duracao['medio'], graus_dificuldade['facil'])
    grau_barato = max(regra1, regra2, regra3)

    # Regras que levam à saída 'justo'
    regra4 = min(graus_duracao['curto'], graus_dificuldade['dificil'])
    regra5 = min(graus_duracao['medio'], graus_dificuldade['media'])
    regra6 = min(graus_duracao['longo'], graus_dificuldade['facil'])
    grau_justo = max(regra4, regra5, regra6)

    # Regras que levam à saída 'caro'
    regra7 = min(graus_duracao['medio'], graus_dificuldade['dificil'])
    regra8 = min(graus_duracao['longo'], graus_dificuldade['media'])
    regra9 = min(graus_duracao['longo'], graus_dificuldade['dificil'])
    grau_caro = max(regra7, regra8, regra9)
    
    return {
        'barato': grau_barato,
        'justo': grau_justo,
        'caro': grau_caro
    }

def defuzzificar(resultados_regras):
    divida = 0.0
    divisor = 0.0
    passo = 10
    
    for x in range(0, 1001, passo):
        pert_barato = pertinencia_triangular(x, 0, 0, 500)
        pert_justo  = pertinencia_triangular(x, 0, 500, 1000)
        pert_caro   = pertinencia_triangular(x, 500, 1000, 1000)
        
        ativacao_barato = min(pert_barato, resultados_regras['barato'])
        ativacao_justo  = min(pert_justo, resultados_regras['justo'])
        ativacao_caro   = min(pert_caro, resultados_regras['caro'])
        
        grau_final = max(ativacao_barato, ativacao_justo, ativacao_caro)
        
        divida += x * grau_final
        divisor += grau_final
        
    # Se nenhuma regra ativou, retornamos zero para evitar divisão por zero
    if divisor == 0:
        return 0.0
        
    return divida / divisor