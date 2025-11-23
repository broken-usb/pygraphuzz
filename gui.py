import tkinter as tk
from tkinter import messagebox
import fuzzy_logic
import graphy

class FuzzyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Orçamento Fuzzy")
        self.root.geometry("400x450")
        
        self.ultimo_duracao = 0
        self.ultimo_dificuldade = 0
        self.calculo_realizado = False

        self.label_titulo = tk.Label(root, text="Orçamento de Serviço", font=("Arial", 16, "bold"))
        self.label_titulo.pack(pady=20)

        self.label_duracao = tk.Label(root, text="Duração do Serviço (horas):", font=("Arial", 10))
        self.label_duracao.pack()

        self.entry_duracao = tk.Entry(root, font=("Arial", 12), justify='center')
        self.entry_duracao.pack(pady=5)

        # Barrinha para escolher a dificuldade
        self.label_dificuldade = tk.Label(root, text="Nível de Dificuldade (0 a 10):", font=("Arial", 10))
        self.label_dificuldade.pack(pady=(15, 0)) # Mais espaço em cima

        self.scale_dificuldade = tk.Scale(root, from_=0, to=10, orient='horizontal', length=300, tickinterval=1)
        self.scale_dificuldade.set(5) # Valor inicial no meio
        self.scale_dificuldade.pack(pady=5)

        # O botao de calcular
        self.btn_calcular = tk.Button(root, text="CALCULAR PREÇO", 
                                      bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                                      command=self.realizar_calculo) # Chama a função ao clicar
        self.btn_calcular.pack(pady=20, ipadx=10, ipady=5)

        # Resultados
        self.label_resultado_titulo = tk.Label(root, text="Valor Sugerido:", font=("Arial", 10))
        self.label_resultado_titulo.pack()

        self.label_valor_final = tk.Label(root, text="R$ 0.00", font=("Arial", 20, "bold"), fg="#333")
        self.label_valor_final.pack(pady=5)

        # O botao dos graficos
        self.btn_grafico = tk.Button(root, text="Ver Gráficos Explicativos", 
                                     command=self.abrir_graficos, state="disabled") # Começa desativado
        self.btn_grafico.pack(pady=20)

        self.footer = tk.Label(root, text="Desenvolvido com Python & Lógica Fuzzy", font=("Arial", 8), fg="gray")
        self.footer.pack(side="bottom", pady=10)

    def realizar_calculo(self):
        try:
            duracao_texto = self.entry_duracao.get()
            
            if not duracao_texto:
                messagebox.showwarning("Atenção", "Por favor, digite a duração do serviço.")
                return

            # Troca a virgula por um ponto, para que o Python consiga entender
            # (Culpa dos Gringos que usam ponto como separador decimal)
            duracao = float(duracao_texto.replace(',', '.'))

            if duracao < 0 or duracao > 24:
                 messagebox.showwarning("Atenção", "A duração deve ser entre 0 e 24 horas.")
                 return

            dificuldade = float(self.scale_dificuldade.get())

            # Efetua os calculos Fuzzy
            graus_dur = fuzzy_logic.calcular_graus_duracao(duracao)
            graus_dif = fuzzy_logic.calcular_graus_dificuldade(dificuldade)
            regras = fuzzy_logic.calcular_regras(graus_dur, graus_dif)
            valor_final = fuzzy_logic.defuzzificar(regras)

            self.label_valor_final.config(text=f"R$ {valor_final:.2f}", fg="#2E7D32")
            
            # Salva tudo e permite o usuario a ver os graficos
            self.ultimo_duracao = duracao
            self.ultimo_dificuldade = dificuldade
            self.calculo_realizado = True
            self.btn_grafico.config(state="normal", bg="#2196F3", fg="white")

        except ValueError:
            messagebox.showerror("Erro", "O valor da duração deve ser numérico.")

    def abrir_graficos(self):
        if self.calculo_realizado:
            graphy.plotar_graficos_reais(self.ultimo_duracao, self.ultimo_dificuldade)

if __name__ == "__main__":
    root = tk.Tk()
    app = FuzzyApp(root)
    root.mainloop()