# Ignorar este arquivo na análise de cobertura de código,
# ele está aqui apenas para testar direto pelo GitHub.
import unittest
import fuzzy_logic


class TestSistemaFuzzy(unittest.TestCase):

    def test_pertinencia_triangular(self):
        # Testa pertinência triangular
        self.assertEqual(fuzzy_logic.pertinencia_triangular(5, 0, 5, 10), 1.0)
        self.assertEqual(fuzzy_logic.pertinencia_triangular(20, 0, 5, 10), 0.0)
        self.assertEqual(fuzzy_logic.pertinencia_triangular(2.5, 0, 5, 10), 0.5)

    def test_duracao_logica(self):
        # Testa conjuntos de duração

        # Curto (0h)
        graus = fuzzy_logic.calcular_graus_duracao(0)
        self.assertEqual(graus['curto'], 1.0, "0h deve ser 100% Curto")

        # Levemente longo (10h)
        graus = fuzzy_logic.calcular_graus_duracao(10)
        self.assertEqual(graus['levemente_longo'], 1.0, "10h deve ser 100% Levemente Longo")

        # Longo (18h)
        graus = fuzzy_logic.calcular_graus_duracao(18)
        self.assertEqual(graus['longo'], 1.0, "18h deve ser 100% Longo")

        # Muito longo (45h)
        graus = fuzzy_logic.calcular_graus_duracao(45)
        self.assertEqual(graus['muito_longo'], 1.0, "45h deve ser 100% Muito Longo")

    def test_logica_preco_extremidades(self):
        # Testa preços nas extremidades

        # Caso 1: mínimo -> barato
        graus_dur = fuzzy_logic.calcular_graus_duracao(0)
        graus_dif = fuzzy_logic.calcular_graus_dificuldade(0)
        regras = fuzzy_logic.calcular_regras(graus_dur, graus_dif)
        valor_minimo = fuzzy_logic.defuzzificar(regras)
        self.assertLess(valor_minimo, 400, "Serviço mínimo deve custar menos de R$ 400")

        # Caso 2: máximo -> muito caro
        graus_dur = fuzzy_logic.calcular_graus_duracao(50)
        graus_dif = fuzzy_logic.calcular_graus_dificuldade(10)
        regras = fuzzy_logic.calcular_regras(graus_dur, graus_dif)
        valor_maximo = fuzzy_logic.defuzzificar(regras)
        self.assertGreater(valor_maximo, 1500, "Serviço máximo deve custar mais de R$ 1500")


if __name__ == '__main__':
    unittest.main()