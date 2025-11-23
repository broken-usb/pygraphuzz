import tkinter as tk
import os
import fuzzy_logic
import graphy
import gui

def limpar_tela():
    # Limpa a tela do terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    # Essse 'if' é para verificar o sistema operacional,
    # como eu uso Linux o comando é 'clear', ja no Windows é 'cls'

def executar_modo_terminal():
    # Modo de execução via terminal
    # Foi utilizado para testar a logica fuzzy antes de implementar a GUI
    janela_escolha.destroy()
    
    while True:
        limpar_tela()
        print("========================================")
        print("    SISTEMA DE ORÇAMENTO                ")
        print("========================================")
        print("Digite 'sair' a qualquer momento para fechar.\n")

        try:
            # Entradas do Usuario
            entrada_duracao = input(">> Digite a Duração (horas): ")
            if entrada_duracao.lower() == 'sair': break
            duracao = float(entrada_duracao)

            if duracao < 0 or duracao > 24:
                print("\n[!] A duração deve ser entre 0 e 24 horas.")
                input("Enter para continuar...")
                continue

            entrada_dificuldade = input(">> Digite a Dificuldade (0-10): ")
            if entrada_dificuldade.lower() == 'sair': break
            dificuldade = float(entrada_dificuldade)
            
            if dificuldade < 0 or dificuldade > 10:
                print("\n[!] A dificuldade deve ser entre 0 e 10.")
                input("Enter para continuar...")
                continue

            # Calculos Fuzzy
            print("\nCalculando...")
            graus_dur = fuzzy_logic.calcular_graus_duracao(duracao)
            graus_dif = fuzzy_logic.calcular_graus_dificuldade(dificuldade)
            regras = fuzzy_logic.calcular_regras(graus_dur, graus_dif)
            preco_final = fuzzy_logic.defuzzificar(regras)

            # Resultados
            print("-" * 40)
            print(f"VALOR SUGERIDO: R$ {preco_final:.2f}")
            print("-" * 40)

            # Plota os Graficos
            ver = input("\nVer gráfico? (s/n): ")
            if ver.lower() == 's':
                graphy.plotar_graficos_reais(duracao, dificuldade)

            input("\nEnter para novo cálculo...")

        except ValueError:
            print("\n[!] Digite apenas números.")
            input("Enter para continuar...")

def executar_modo_grafico():
    # Fecha a janela de escolha e
    # abre a interface grafica
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