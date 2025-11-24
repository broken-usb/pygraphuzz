def pertinencia_triangular(x, a, b, c):
    # Função triangular de pertinência.
    # Retorna um valor entre 0 e 1 indicando o quanto `x` pertence
    # ao conjunto definido pelo triângulo (a, b, c).
    if x == b: return 1.0
    if x <= a or x >= c: return 0.0
    if a < x < b: return (x - a) / (b - a)
    if b < x < c: return (c - x) / (c - b)
    return 0.0

def pertinencia_trapezoidal(x, a, b, c, d):
    # Função trapezoidal de pertinência.
    # Produz valores entre 0 e 1 com um platô (valor 1) entre b e c.
    # Útil quando queremos um intervalo totalmente pertencente ao conjunto.
    if x <= a or x >= d: return 0.0
    if b <= x <= c: return 1.0
    if a < x < b: return (x - a) / (b - a)
    if c < x < d: return (d - x) / (d - c)
    return 0.0

def calcular_graus_duracao(tempo):
    # Calcula os graus de pertinência para as etiquetas de duração.
    # Retorna um dict com os graus para: 'curto', 'levemente_longo',
    # 'longo' e 'muito_longo'. Esses valores ficam entre 0 e 1.
    graus = {}

    # 'curto' -> trapézio à esquerda: valores <= 0 são totalmente curtos,
    # decaindo até 8h.
    graus['curto'] = pertinencia_trapezoidal(tempo, -100, 0, 0, 8)

    # 'levemente_longo' -> pico em 10h, começa a subir em 6 e desce a partir de 14.
    graus['levemente_longo'] = pertinencia_triangular(tempo, 6, 10, 14)

    # 'longo' -> pico em 18h, usado para trabalhos mais demorados.
    graus['longo'] = pertinencia_triangular(tempo, 12, 18, 24)

    # 'muito_longo' -> trapézio à direita: sobe entre 20 e 40 e fica 1 a partir daí.
    graus['muito_longo'] = pertinencia_trapezoidal(tempo, 20, 40, 100, 100)

    return graus

def calcular_graus_dificuldade(nivel):
    # Calcula os graus de pertinência para dificuldade.
    # Retorna dict com: 'facil', 'media', 'dificil'.
    graus = {}
    # 'facil' -> trapézio à esquerda (0 é totalmente fácil)
    graus['facil'] = pertinencia_trapezoidal(nivel, -10, 0, 0, 5)

    # 'media' -> triangular com pico em 5
    graus['media'] = pertinencia_triangular(nivel, 0, 5, 10)

    # 'dificil' -> trapézio à direita (10+ tende a ser difícil)
    graus['dificil'] = pertinencia_trapezoidal(nivel, 5, 10, 20, 20)
    return graus

def calcular_regras(graus_dur, graus_dif):
    # Avalia regras simples em forma Mamdani.
    # Usamos `min` para AND e `max` para combinar diferentes regras (OR).
    grau_barato = 0.0
    grau_justo = 0.0
    grau_caro = 0.0
    grau_muito_caro = 0.0

    # Regras que levam a 'barato'
    r1 = min(graus_dur['curto'], graus_dif['facil'])
    r2 = min(graus_dur['curto'], graus_dif['media'])
    r3 = min(graus_dur['levemente_longo'], graus_dif['facil'])
    grau_barato = max(r1, r2, r3)

    # Regras que levam a 'justo'
    r4 = min(graus_dur['curto'], graus_dif['dificil'])
    r5 = min(graus_dur['levemente_longo'], graus_dif['media'])
    r6 = min(graus_dur['levemente_longo'], graus_dif['dificil'])
    r7 = min(graus_dur['longo'], graus_dif['facil'])
    grau_justo = max(r4, r5, r6, r7)

    # Regras que levam a 'caro'
    r8 = min(graus_dur['longo'], graus_dif['media'])
    r9 = min(graus_dur['longo'], graus_dif['dificil'])
    r10 = min(graus_dur['muito_longo'], graus_dif['facil'])
    r11 = min(graus_dur['muito_longo'], graus_dif['media'])
    grau_caro = max(r8, r9, r10, r11)

    # Regras que levam a 'muito_caro'
    r12 = min(graus_dur['muito_longo'], graus_dif['dificil'])
    grau_muito_caro = r12

    return {
        'barato': grau_barato,
        'justo': grau_justo,
        'caro': grau_caro,
        'muito_caro': grau_muito_caro
    }

def defuzzificar(resultados_regras):
    # Defuzzificação por centróide (método discreto).
    # Varremos o universo de saída (preço) somando x * grau e dividindo
    # pela soma dos graus para obter o centro de massa.
    divida = 0.0
    divisor = 0.0
    passo = 20

    for x in range(0, 2001, passo):
        # Funções de saída aproximadas para cada rótulo de preço
        pert_barato = pertinencia_trapezoidal(x, -500, 0, 0, 600)
        pert_justo  = pertinencia_triangular(x, 400, 800, 1200)
        pert_caro   = pertinencia_triangular(x, 1000, 1400, 1800)
        pert_mcaro  = pertinencia_trapezoidal(x, 1600, 2000, 3000, 3000)

        # "Corta" cada função pelo nível de ativação da regra (Mamdani)
        atv_barato = min(pert_barato, resultados_regras['barato'])
        atv_justo  = min(pert_justo, resultados_regras['justo'])
        atv_caro   = min(pert_caro, resultados_regras['caro'])
        atv_mcaro  = min(pert_mcaro, resultados_regras['muito_caro'])

        # União das saídas ativadas (máximo)
        grau_final = max(atv_barato, atv_justo, atv_caro, atv_mcaro)

        divida += x * grau_final
        divisor += grau_final

    if divisor == 0: return 0.0
    return divida / divisor