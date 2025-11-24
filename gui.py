import tkinter as tk
from tkinter import ttk  # Widgets com suporte a temas
from tkinter import messagebox
import fuzzy_logic
import graphy

class FuzzyApp:
    # Interface gráfica minimalista para testar entradas e visualizar o resultado
    def __init__(self, root):
        self.root = root
        self.root.title("PyGraphUzz | TKinter")
        self.root.geometry("420x600") 
        
        # Paleta de cores (tudo centralizado aqui para ajuste rápido)
        self.COLOR_BG = "#242424"       # cor do fundo da janela
        self.COLOR_FG = "#ffffff"       # cor do texto
        self.COLOR_ACCENT = "#3584e4"   # cor de destaque (ações principais)
        self.COLOR_SUCCESS = "#2ec27e"  # cor usada para resultados positivos
        self.COLOR_SURFACE = "#303030"  # cor para superfícies e campos
        
        self.root.configure(bg=self.COLOR_BG)

        # Configurações de estilo do ttk (tema e aparência)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # Estilo genérico aplicado a widgets
        self.style.configure(".", background=self.COLOR_BG, foreground=self.COLOR_FG, font=("Segoe UI", 10))

        # Aparência da Treeview (janela de regras) — deixa com o mesmo tom de superfície
        self.style.configure("Treeview", background=self.COLOR_SURFACE, foreground=self.COLOR_FG, fieldbackground=self.COLOR_SURFACE, borderwidth=0)
        self.style.map('Treeview', background=[('selected', self.COLOR_ACCENT)], foreground=[('selected', 'white')])

        # Botões: principal (Accent) e secundários
        self.style.configure("Accent.TButton", background=self.COLOR_ACCENT, foreground="white", borderwidth=0, focuscolor=self.COLOR_ACCENT)
        self.style.map("Accent.TButton", background=[('active', '#1c71d8')])
        self.style.configure("Secondary.TButton", background=self.COLOR_SURFACE, foreground=self.COLOR_FG, borderwidth=0)
        self.style.map("Secondary.TButton", background=[('active', '#454545')])

        self.ultimo_duracao = 0
        self.ultimo_dificuldade = 0
        self.calculo_realizado = False

        # Layout principal: campos de entrada, botões e área de resultado
        main_frame = ttk.Frame(root, padding=25)
        main_frame.pack(fill="both", expand=True)

        # Título
        self.label_titulo = ttk.Label(main_frame, text="Orçamento de Serviço", font=("Segoe UI", 18, "bold"))
        self.label_titulo.pack(pady=(0, 20))

        # Input 1: duração do serviço (horas)
        self.label_duracao = ttk.Label(main_frame, text="Duração do Serviço (0 a 42h):")
        self.label_duracao.pack(anchor="w")

        self.entry_duracao = tk.Entry(main_frame, font=("Segoe UI", 12), justify='center',
                                      bg=self.COLOR_SURFACE, fg=self.COLOR_FG, 
                                      insertbackground="white", relief="flat", bd=8)
        self.entry_duracao.pack(pady=(5, 15), fill="x")

        # Input 2: dificuldade (slider de 0 a 10)
        self.label_dificuldade = ttk.Label(main_frame, text="Nível de Dificuldade (0 a 10):")
        self.label_dificuldade.pack(anchor="w")

        self.scale_dificuldade = tk.Scale(main_frame, from_=0, to=10, orient='horizontal', 
                                          bg=self.COLOR_BG, fg=self.COLOR_FG, troughcolor=self.COLOR_SURFACE,
                                          highlightthickness=0, activebackground=self.COLOR_ACCENT,
                                          relief="flat", font=("Segoe UI", 9))
        self.scale_dificuldade.set(5)
        self.scale_dificuldade.pack(pady=(5, 15), fill="x")

        # Botão principal que aciona o cálculo
        self.btn_calcular = ttk.Button(main_frame, text="CALCULAR PREÇO", style="Accent.TButton",
                           command=self.realizar_calculo)
        self.btn_calcular.pack(pady=10, fill="x", ipady=5)

        # Área de resultado
        self.label_resultado_titulo = ttk.Label(main_frame, text="Valor Sugerido:", font=("Segoe UI", 10))
        self.label_resultado_titulo.pack(pady=(15, 0))

        self.label_valor_final = ttk.Label(main_frame, text="R$ ---", font=("Segoe UI", 26, "bold"), foreground=self.COLOR_FG)
        self.label_valor_final.pack(pady=5)

        # Botões Extras
        self.btn_grafico = ttk.Button(main_frame, text="Ver Gráficos Explicativos", style="Secondary.TButton",
                                      command=self.abrir_graficos, state="disabled")
        self.btn_grafico.pack(pady=(15, 5), fill="x")

        self.btn_regras = ttk.Button(main_frame, text="Ver Regras do Sistema", style="Secondary.TButton",
                                     command=self.mostrar_regras)
        self.btn_regras.pack(pady=5, fill="x")

    def realizar_calculo(self):
        try:
            duracao_texto = self.entry_duracao.get()
            if not duracao_texto:
                messagebox.showwarning("Atenção", "Por favor, digite a duração.")
                return

            duracao = float(duracao_texto.replace(',', '.'))
            
            if duracao < 0 or duracao > 42:
                 messagebox.showwarning("Atenção", "A duração deve ser entre 0 e 42 horas.")
                 return

            dificuldade = float(self.scale_dificuldade.get())

            # Executa o motor fuzzy: calcula graus, aplica regras e defuzzifica
            graus_dur = fuzzy_logic.calcular_graus_duracao(duracao)
            graus_dif = fuzzy_logic.calcular_graus_dificuldade(dificuldade)
            regras = fuzzy_logic.calcular_regras(graus_dur, graus_dif)
            valor_final = fuzzy_logic.defuzzificar(regras)

            self.label_valor_final.config(text=f"R$ {valor_final:.2f}", foreground=self.COLOR_SUCCESS)
            
            self.ultimo_duracao = duracao
            self.ultimo_dificuldade = dificuldade
            self.calculo_realizado = True
            self.btn_grafico.config(state="normal")

        except ValueError:
            messagebox.showerror("Erro", "O valor da duração deve ser numérico.")

    def abrir_graficos(self):
        if self.calculo_realizado:
            graphy.plotar_graficos_reais(self.ultimo_duracao, self.ultimo_dificuldade)

    def mostrar_regras(self):
        """Abre uma janela com a base de conhecimento e regras do sistema.

        A janela usa uma Treeview para listar categorias (Tempo, Dificuldade, Preço)
        e as regras que ligam entradas às saídas. Útil para entender como o
        sistema está classifying e combinando termos fuzzy.
        """
        janela_regras = tk.Toplevel(self.root)
        janela_regras.title("Base de Conhecimento do Sistema")
        janela_regras.geometry("500x600")
        janela_regras.configure(bg=self.COLOR_BG)

        lbl_titulo = ttk.Label(janela_regras, text="Regras e Definições", font=("Segoe UI", 14, "bold"))
        lbl_titulo.pack(pady=10)

        tree = ttk.Treeview(janela_regras, show="tree", height=20)
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # CATEGORIA 1: TEMPO
        pai_tempo = tree.insert("", "end", iid="cat_tempo", text="Definições de Tempo", open=False)
        tree.insert(pai_tempo, "end", text="• Curto: <0 - 8")
        tree.insert(pai_tempo, "end", text="• Levemente Longo: 6 - 14 (Media = 10)")
        tree.insert(pai_tempo, "end", text="• Longo: 12 - 24 (Media = 18)")
        tree.insert(pai_tempo, "end", text="• Muito Longo: >20")

        # CATEGORIA 2: DIFICULDADE
        pai_dif = tree.insert("", "end", iid="cat_dif", text="Definições de Dificuldade", open=False)
        tree.insert(pai_dif, "end", text="• Fácil: <0 - 5")
        tree.insert(pai_dif, "end", text="• Média: 0 - 10 (Media = 5)")
        tree.insert(pai_dif, "end", text="• Difícil: >5")

        # CATEGORIA 3: PREÇO
        pai_preco = tree.insert("", "end", iid="cat_preco", text="Definições de Preço", open=False)
        tree.insert(pai_preco, "end", text="• Barato: <0 - 600")
        tree.insert(pai_preco, "end", text="• Justo: 400 - 1.200")
        tree.insert(pai_preco, "end", text="• Caro: 1.000,00 - 1.800,00")
        tree.insert(pai_preco, "end", text="• Muito Caro: >1.600,00")

        # CATEGORIA 4: REGRAS
        pai_regras = tree.insert("", "end", iid="cat_regras", text="Regras da Saida (Preço)", open=True)
        
        pai_barato = tree.insert(pai_regras, "end", text="Saida = BARATO", open=True)
        tree.insert(pai_barato, "end", text="SE (Curto E Fácil)")
        tree.insert(pai_barato, "end", text="SE (Curto E Média)")
        tree.insert(pai_barato, "end", text="SE (Levemente Longo E Fácil)")

        pai_justo = tree.insert(pai_regras, "end", text="Saida = JUSTO", open=False)
        tree.insert(pai_justo, "end", text="SE (Curto E Difícil)")
        tree.insert(pai_justo, "end", text="SE (Levemente Longo E Média)")
        tree.insert(pai_justo, "end", text="SE (Levemente Longo E Difícil)")
        tree.insert(pai_justo, "end", text="SE (Longo E Fácil)")

        pai_caro = tree.insert(pai_regras, "end", text="Saida = CARO", open=False)
        tree.insert(pai_caro, "end", text="SE (Longo E Média)")
        tree.insert(pai_caro, "end", text="SE (Longo E Difícil)")
        tree.insert(pai_caro, "end", text="SE (Muito Longo E Fácil)")
        tree.insert(pai_caro, "end", text="SE (Muito Longo E Média)")

        pai_mcaro = tree.insert(pai_regras, "end", text="Saida = MUITO CARO", open=False)
        tree.insert(pai_mcaro, "end", text="SE (Muito Longo E Difícil)")

if __name__ == "__main__":
    root = tk.Tk()
    app = FuzzyApp(root)
    root.mainloop()