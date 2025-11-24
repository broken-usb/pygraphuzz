import unittest
import fuzzy_logic

class TestSistemaFuzzy(unittest.TestCase):

    def test_pertinencia_triangular(self):
        # Verifica alguns pontos simples na função triangular
        self.assertEqual(fuzzy_logic.pertinencia_triangular(5, 0, 5, 10), 1.0)
        self.assertEqual(fuzzy_logic.pertinencia_triangular(20, 0, 5, 10), 0.0)
        self.assertEqual(fuzzy_logic.pertinencia_triangular(2.5, 0, 5, 10), 0.5)

    def test_pertinencia_trapezoidal(self):
        # Testa forma trapezoidal: sobe, plateau, desce
        # Parâmetros do trapézio: a=0, b=10, c=20, d=30

        # Antes do início -> zero
        self.assertEqual(fuzzy_logic.pertinencia_trapezoidal(-5, 0, 10, 20, 30), 0.0)

        # Subida (5 está a meio entre 0 e 10)
        self.assertEqual(fuzzy_logic.pertinencia_trapezoidal(5, 0, 10, 20, 30), 0.5)

        # Platô (15 entre 10 e 20)
        self.assertEqual(fuzzy_logic.pertinencia_trapezoidal(15, 0, 10, 20, 30), 1.0)

        # Descida (25 a meio entre 20 e 30)
        self.assertEqual(fuzzy_logic.pertinencia_trapezoidal(25, 0, 10, 20, 30), 0.5)

        # Depois do fim -> zero
        self.assertEqual(fuzzy_logic.pertinencia_trapezoidal(35, 0, 10, 20, 30), 0.0)

    def test_duracao_logica(self):
        # Verifica rótulos principais em pontos representativos
        graus = fuzzy_logic.calcular_graus_duracao(0)
        self.assertEqual(graus['curto'], 1.0)

        graus = fuzzy_logic.calcular_graus_duracao(10)
        self.assertEqual(graus['levemente_longo'], 1.0)

        graus = fuzzy_logic.calcular_graus_duracao(18)
        self.assertEqual(graus['longo'], 1.0)

        graus = fuzzy_logic.calcular_graus_duracao(45)
        self.assertEqual(graus['muito_longo'], 1.0)

    def test_logica_preco_extremidades(self):
        # Cenário: entradas que devem produzir preço baixo
        graus_dur = fuzzy_logic.calcular_graus_duracao(0)
        graus_dif = fuzzy_logic.calcular_graus_dificuldade(0)
        regras = fuzzy_logic.calcular_regras(graus_dur, graus_dif)
        valor_minimo = fuzzy_logic.defuzzificar(regras)
        self.assertLess(valor_minimo, 400)

        # Cenário: entradas que devem produzir preço alto
        graus_dur = fuzzy_logic.calcular_graus_duracao(50)
        graus_dif = fuzzy_logic.calcular_graus_dificuldade(10)
        regras = fuzzy_logic.calcular_regras(graus_dur, graus_dif)
        valor_maximo = fuzzy_logic.defuzzificar(regras)
        self.assertGreater(valor_maximo, 1500)

if __name__ == '__main__':
    unittest.main()