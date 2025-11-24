import tkinter as tk
from tkinter import ttk  # Widgets com suporte a temas
from tkinter import messagebox
import fuzzy_logic
import graphy

class FuzzyApp:
    # GUI principal do app — simples e direta para testar o motor fuzzy
    def __init__(self, root):
        self.root = root
        self.root.title("PyGraphUzz | TKinter")
        self.root.geometry("420x550") 
        
        # Paleta de cores da interface (centralizada para ajustar fácil)
        self.COLOR_BG = "#242424"
        self.COLOR_FG = "#ffffff"
        self.COLOR_ACCENT = "#3584e4"
        self.COLOR_SUCCESS = "#2ec27e"
        self.COLOR_SURFACE = "#303030"
        self.COLOR_BORDER = "#1b1b1b"
        
        # Ajusta o fundo da janela
        self.root.configure(bg=self.COLOR_BG)

        # Estilos (ttk)
        self.style = ttk.Style()
        self.style.theme_use('clam') # 'clam' permite maior customização de cores

        # Estilo base do ttk (fonte, cores padrão)
        self.style.configure(".", 
                             background=self.COLOR_BG, 
                             foreground=self.COLOR_FG, 
                             font=("Segoe UI", 10))

        # Estilo do botão principal (ação de calcular)
        self.style.configure("Accent.TButton", 
                             background=self.COLOR_ACCENT, 
                             foreground="white",
                             borderwidth=0,
                             focuscolor=self.COLOR_ACCENT)
        # Pequeno efeito visual ao passar o mouse
        self.style.map("Accent.TButton", 
                       background=[('active', '#1c71d8')]) 

        # Estilo para botões secundários (ver gráficos, etc.)
        self.style.configure("Secondary.TButton", 
                             background=self.COLOR_SURFACE, 
                             foreground=self.COLOR_FG,
                             borderwidth=0)
        self.style.map("Secondary.TButton", 
                       background=[('active', '#454545')])

        # Estado interno da UI (últimos valores e se já calculou)
        self.ultimo_duracao = 0
        self.ultimo_dificuldade = 0
        self.calculo_realizado = False

        # Monta a interface: frame principal, inputs, botões e resultado
        
        # Frame principal que segura tudo
        main_frame = ttk.Frame(root, padding=25)
        main_frame.pack(fill="both", expand=True)

        # Título
        self.label_titulo = ttk.Label(main_frame, text="Orçamento de Serviço", font=("Segoe UI", 18, "bold"))
        self.label_titulo.pack(pady=(0, 25))

        # Rótulo para entrada de duração
        self.label_duracao = ttk.Label(main_frame, text="Duração do Serviço (0 a 42h):")
        self.label_duracao.pack(anchor="w")

        # Campo de texto para digitar a duração (aceita vírgula)
        self.entry_duracao = tk.Entry(main_frame, font=("Segoe UI", 12), justify='center',
                                      bg=self.COLOR_SURFACE, fg=self.COLOR_FG, 
                                      insertbackground="white", # Cor do cursor
                                      relief="flat", bd=8)      # Borda interna (padding fake)
        self.entry_duracao.pack(pady=(5, 20), fill="x")

        # Rótulo para a escala de dificuldade
        self.label_dificuldade = ttk.Label(main_frame, text="Nível de Dificuldade (0 a 10):")
        self.label_dificuldade.pack(anchor="w")

        # Controle tipo slider para ajustar a dificuldade (visual e rápido)
        self.scale_dificuldade = tk.Scale(main_frame, from_=0, to=10, orient='horizontal', 
                                          bg=self.COLOR_BG, fg=self.COLOR_FG,
                                          troughcolor=self.COLOR_SURFACE, # Cor do trilho
                                          highlightthickness=0,           # Remove borda de foco feia
                                          activebackground=self.COLOR_ACCENT,
                                          relief="flat",
                                          font=("Segoe UI", 9))
        self.scale_dificuldade.set(5)
        self.scale_dificuldade.pack(pady=(5, 20), fill="x")

        # Botão que dispara o cálculo fuzzy
        self.btn_calcular = ttk.Button(main_frame, text="CALCULAR PREÇO", 
                                       style="Accent.TButton",
                                       command=self.realizar_calculo)
        self.btn_calcular.pack(pady=10, fill="x", ipady=5)

        # Área que mostra o resultado do cálculo
        self.label_resultado_titulo = ttk.Label(main_frame, text="Valor Sugerido:", font=("Segoe UI", 10))
        self.label_resultado_titulo.pack(pady=(20, 0))

        self.label_valor_final = ttk.Label(main_frame, text="R$ ---", 
                                           font=("Segoe UI", 26, "bold"), 
                                           foreground=self.COLOR_FG)
        self.label_valor_final.pack(pady=5)

        # Botão para abrir os gráficos explicativos (desativado até calcular)
        self.btn_grafico = ttk.Button(main_frame, text="Ver Gráficos Explicativos", 
                                      style="Secondary.TButton",
                                      command=self.abrir_graficos, state="disabled")
        self.btn_grafico.pack(pady=15, fill="x")

        # Rodapé
        self.footer = ttk.Label(main_frame, text="Lógica Fuzzy v1.0", font=("Segoe UI", 8), foreground="#666666")
        self.footer.pack(side="bottom")

    def realizar_calculo(self):
        try:
            duracao_texto = self.entry_duracao.get()
            
            if not duracao_texto:
                # Peça educadamente para o usuário preencher
                messagebox.showwarning("Atenção", "Por favor, digite a duração do serviço.")
                return

            duracao = float(duracao_texto.replace(',', '.'))

            # Validação simples da faixa permitida
            if duracao < 0 or duracao > 42:
                messagebox.showwarning("Atenção", "A duração deve ser entre 0 e 42 horas.")
                return

            dificuldade = float(self.scale_dificuldade.get())

            # Roda o motor fuzzy e pega o valor defuzzificado
            graus_dur = fuzzy_logic.calcular_graus_duracao(duracao)
            graus_dif = fuzzy_logic.calcular_graus_dificuldade(dificuldade)
            regras = fuzzy_logic.calcular_regras(graus_dur, graus_dif)
            valor_final = fuzzy_logic.defuzzificar(regras)

            # Mostra o resultado
            self.label_valor_final.config(text=f"R$ {valor_final:.2f}", foreground=self.COLOR_SUCCESS)
            
            self.ultimo_duracao = duracao
            self.ultimo_dificuldade = dificuldade
            self.calculo_realizado = True
            self.btn_grafico.config(state="normal") # O estilo visual já indica que ativou

        except ValueError:
            # Aviso amigável quando o dado não é numérico
            messagebox.showerror("Erro", "O valor da duração deve ser numérico.")

    def abrir_graficos(self):
        if self.calculo_realizado:
            # Abre os gráficos explicativos usando os últimos inputs
            graphy.plotar_graficos_reais(self.ultimo_duracao, self.ultimo_dificuldade)

if __name__ == "__main__":
    root = tk.Tk()
    app = FuzzyApp(root)
    root.mainloop()