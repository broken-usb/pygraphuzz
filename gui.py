import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import fuzzy_logic
import graphy

class FuzzyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PyGraphUzz | TKinter")
        self.root.geometry("420x580")
        
        # Define as cores do TKinter
        self.COLOR_BG = "#242424"
        self.COLOR_FG = "#ffffff"
        self.COLOR_ACCENT = "#3584e4"
        self.COLOR_SUCCESS = "#2ec27e"
        self.COLOR_SURFACE = "#303030"
        self.root.configure(bg=self.COLOR_BG)
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.configure(".", 
                             background=self.COLOR_BG, 
                             foreground=self.COLOR_FG, 
                             font=("Segoe UI", 10)) # Fonte mais limpa

        # Estilo para os botões
        # Principais
        self.style.configure("Accent.TButton", 
                             background=self.COLOR_ACCENT, 
                             foreground="white",
                             borderwidth=0,
                             focuscolor=self.COLOR_ACCENT)
        self.style.map("Accent.TButton", 
                       background=[('active', '#1c71d8')]) # Azul mais escuro ao passar o mouse

        # Graficos
        self.style.configure("Secondary.TButton", 
                             background=self.COLOR_SURFACE, 
                             foreground=self.COLOR_FG,
                             borderwidth=0)
        self.style.map("Secondary.TButton", 
                       background=[('active', '#454545')])

        # Outros
        self.style.configure("TRadiobutton", 
                             indicatorcolor=self.COLOR_ACCENT,
                             indicatoron=True)

        self.ultimo_duracao = 0
        self.ultimo_dificuldade = 0
        self.calculo_realizado = False

        # Parte da Interface
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill="both", expand=True)

        self.label_titulo = ttk.Label(main_frame, text="Orçamento de Serviço", font=("Segoe UI", 18, "bold"))
        self.label_titulo.pack(pady=(0, 20))

        # Entrada 1: Duração
        self.label_duracao = ttk.Label(main_frame, text="Duração do Serviço (0 a 24h):")
        self.label_duracao.pack(anchor="w") # Alinhado a esquerda

        self.entry_duracao = tk.Entry(main_frame, font=("Segoe UI", 12), justify='center',
                                      bg=self.COLOR_SURFACE, fg=self.COLOR_FG, 
                                      insertbackground="white", # Cor do cursor
                                      relief="flat", bd=5) # Borda interna para padding
        self.entry_duracao.pack(pady=(5, 15), fill="x")

        # Entrada 2: Dificuldade
        self.label_dificuldade = ttk.Label(main_frame, text="Nível de Dificuldade (0 a 10):")
        self.label_dificuldade.pack(anchor="w")
        self.scale_dificuldade = tk.Scale(main_frame, from_=0, to=10, orient='horizontal', 
                                          bg=self.COLOR_BG, fg=self.COLOR_FG,
                                          troughcolor=self.COLOR_SURFACE,
                                          highlightthickness=0,
                                          activebackground=self.COLOR_ACCENT,
                                          relief="flat",
                                          font=("Segoe UI", 9))
        self.scale_dificuldade.set(5)
        self.scale_dificuldade.pack(pady=(5, 15), fill="x")

        # Escolha de Metodo
        self.label_metodo = ttk.Label(main_frame, text="Método de Inferência:", font=("Segoe UI", 10, "bold"))
        self.label_metodo.pack(pady=(10, 5))
        
        self.metodo_var = tk.StringVar(value="minimo")
        
        frame_radio = ttk.Frame(main_frame)
        frame_radio.pack(pady=5)
        
        ttk.Radiobutton(frame_radio, text="Mínimização", variable=self.metodo_var, 
                       value="minimo").pack(side="left", padx=15)
        
        ttk.Radiobutton(frame_radio, text="Maximização", variable=self.metodo_var, 
                       value="maxino").pack(side="left", padx=15)

        self.btn_calcular = ttk.Button(main_frame, text="CALCULAR PREÇO", 
                                       style="Accent.TButton",
                                       command=self.realizar_calculo)
        self.btn_calcular.pack(pady=25, fill="x", ipady=5)

        self.label_resultado_titulo = ttk.Label(main_frame, text="Valor Sugerido:")
        self.label_resultado_titulo.pack()

        self.label_valor_final = ttk.Label(main_frame, text="R$ 0.00", 
                                           font=("Segoe UI", 24, "bold"), 
                                           foreground=self.COLOR_FG)
        self.label_valor_final.pack(pady=5)

        self.btn_grafico = ttk.Button(main_frame, text="Ver Gráficos Explicativos", 
                                      style="Secondary.TButton",
                                      command=self.abrir_graficos, state="disabled")
        self.btn_grafico.pack(pady=10, fill="x")

        self.footer = ttk.Label(main_frame, text="Projeto de Lógica Fuzzy v1.0", font=("Segoe UI", 8), foreground="gray")
        self.footer.pack(side="bottom", pady=5)

    def realizar_calculo(self):
        try:
            duracao_texto = self.entry_duracao.get()
            if not duracao_texto:
                messagebox.showwarning("Atenção", "Por favor, digite a duração.")
                return

            duracao = float(duracao_texto.replace(',', '.'))
            if duracao < 0 or duracao > 24:
                 messagebox.showwarning("Atenção", "A duração deve ser entre 0 e 24 horas.")
                 return

            dificuldade = float(self.scale_dificuldade.get())
            metodo_escolhido = self.metodo_var.get()

            # Cálculos
            graus_dur = fuzzy_logic.calcular_graus_duracao(duracao)
            graus_dif = fuzzy_logic.calcular_graus_dificuldade(dificuldade)
            regras = fuzzy_logic.calcular_regras(graus_dur, graus_dif)
            valor_final = fuzzy_logic.defuzzificar(regras, metodo=metodo_escolhido)

            self.label_valor_final.config(text=f"R$ {valor_final:.2f}", foreground=self.COLOR_SUCCESS)
            
            self.ultimo_duracao = duracao
            self.ultimo_dificuldade = dificuldade
            self.calculo_realizado = True
            self.btn_grafico.config(state="normal")

        except ValueError:
            messagebox.showerror("Erro", "O valor da duração deve ser numérico.")

    def abrir_graficos(self):
        if self.calculo_realizado:
            graphy.plotar_graficos_reais(self.ultimo_duracao, 
                                         self.ultimo_dificuldade, 
                                         metodo=self.metodo_var.get())

if __name__ == "__main__":
    root = tk.Tk()
    app = FuzzyApp(root)
    root.mainloop()