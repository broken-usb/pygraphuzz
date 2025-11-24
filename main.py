import tkinter as tk
import os
import fuzzy_logic
import graphy
import gui

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def executar_modo_terminal():
    janela_escolha.destroy()
    
    while True:
        limpar_tela()
        print("================")
        print("PyGraphUzz - CLI")
        print("================")
        print("Digite 'sair' a qualquer momento para fechar.\n")

        try:
            # entrada do usuário
            entrada_duracao = input(">> Digite a Duração (horas): ")
            if entrada_duracao.lower() == 'sair': break
            duracao = float(entrada_duracao)

            # Limite: o sistema trabalha entre 0 e 42 horas
            if duracao < 0 or duracao > 42:
                print("\n[!] A duração deve ser entre 0 e 42 horas.")
                input("Enter para continuar...")
                continue

            entrada_dificuldade = input(">> Digite a Dificuldade (0-10): ")
            if entrada_dificuldade.lower() == 'sair': break
            dificuldade = float(entrada_dificuldade)
            
            # Validação simples para dificuldade (0-10)
            if dificuldade < 0 or dificuldade > 10:
                print("\n[!] A dificuldade deve ser entre 0 e 10.")
                input("Enter para continuar...")
                continue

            # Executa o motor fuzzy e apresenta resultado
            print("\nCalculando...")
            graus_dur = fuzzy_logic.calcular_graus_duracao(duracao)
            graus_dif = fuzzy_logic.calcular_graus_dificuldade(dificuldade)
            regras = fuzzy_logic.calcular_regras(graus_dur, graus_dif)
            preco_final = fuzzy_logic.defuzzificar(regras)

            print("-" * 40)
            print(f"VALOR SUGERIDO: R$ {preco_final:.2f}")
            print("-" * 40)

            # Pergunta se o usuário quer ver uma explicação visual
            ver = input("\nVer gráfico? (s/n): ")
            if ver.lower() == 's':
                graphy.plotar_graficos_reais(duracao, dificuldade)

            input("\nEnter para novo cálculo...")

        except ValueError:
            print("\n[!] Digite apenas números.")
            input("Enter para continuar...")

def executar_modo_grafico():
    janela_escolha.destroy()
    root_app = tk.Tk()
    app = gui.FuzzyApp(root_app)
    root_app.mainloop()

def iniciar_launcher():
    global janela_escolha
    janela_escolha = tk.Tk()
    janela_escolha.title("Launcher")
    janela_escolha.geometry("300x150")
    
    lbl = tk.Label(janela_escolha, text="Escolha o modo de inicialização:", font=("Arial", 10))
    lbl.pack(pady=15)
    
    frame_botoes = tk.Frame(janela_escolha)
    frame_botoes.pack()
    
    btn_gui = tk.Button(frame_botoes, text="Interface Gráfica", width=15, bg="#2196F3", fg="white",
                        command=executar_modo_grafico)
    btn_gui.pack(side="left", padx=5)
    
    btn_cli = tk.Button(frame_botoes, text="Modo Terminal", width=15, bg="#555", fg="white",
                        command=executar_modo_terminal)
    btn_cli.pack(side="right", padx=5)
    
    janela_escolha.mainloop()

if __name__ == "__main__":
    iniciar_launcher()