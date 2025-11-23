# Ignore esse arquivo, ele serve para que eu possa testar o
# projeto utilizando o sistema de "Workflows" do GitHub.
import unittest
import fuzzy_logic

class TestSistemaFuzzy(unittest.TestCase):

    def test_pertinencia_triangular(self):
        self.assertEqual(fuzzy_logic.pertinencia_triangular(5, 0, 5, 10), 1.0)
        self.assertEqual(fuzzy_logic.pertinencia_triangular(20, 0, 5, 10), 0.0)
        self.assertEqual(fuzzy_logic.pertinencia_triangular(2.5, 0, 5, 10), 0.5)

    def test_duracao_logica(self):
        graus = fuzzy_logic.calcular_graus_duracao(0)
        self.assertEqual(graus['curto'], 1.0)
        
        graus = fuzzy_logic.calcular_graus_duracao(12)
        self.assertEqual(graus['medio'], 1.0)

        graus = fuzzy_logic.calcular_graus_duracao(24)
        self.assertEqual(graus['longo'], 1.0)

    def test_logica_preco(self):    
        graus_dur = fuzzy_logic.calcular_graus_duracao(0)
        graus_dif = fuzzy_logic.calcular_graus_dificuldade(0)
        regras = fuzzy_logic.calcular_regras(graus_dur, graus_dif)
        valor = fuzzy_logic.defuzzificar(regras)

        self.assertLess(valor, 350)

if __name__ == '__main__':
    unittest.main()