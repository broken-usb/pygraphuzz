## Pré-requisitos

* [Python](https://www.python.org/) 3.12.3 ou superior.
* [Git](https://git-scm.com/) (Para clonar o repositório).

## Como baixar e rodar o projeto

Siga os passos abaixo para configurar o ambiente no seu computador.

### 1. Clonar o Repositório

Abra o seu terminal no local que deseja baixar o projeto e execute:

```bash
git clone "https://github.com/broken-usb/pygraphuzz.git"
```

### 2 Criar o Ambiente Virtual (.venv)

É recomendável criar um ambiente virtual para não misturar as dependências.

  * **Linux / macOS:**

    ```bash
    python3 -m venv .venv
    ```

  * **Windows:**

    ```cmd
    python -m venv .venv
    ```

### Ativar o Ambiente Virtual

  * **Linux / macOS:**

    ```bash
    source .venv/bin/activate
    ```

  * **Windows (CMD):**

    ```cmd
    .venv\Scripts\activate.bat
    ```

  * **Windows (PowerShell):**

    ```powershell
    .venv\Scripts\Activate.ps1
    ```

### Instalar as Dependências

Com o ambiente ativado instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

## Como Executar

Para iniciar o programa, execute o arquivo principal. Um menu será exibido perguntando se deseja iniciar a **Interface Gráfica** ou o **Modo Terminal**.

```bash
python main.py
```
