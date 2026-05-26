# CartolIF - Fantasy Game do JIFBA

CartolIF é uma aplicação web de *fantasy game* desenvolvida para os Jogos Internos do IFBA (JIFBA) - Campus Irecê. A plataforma permite que os usuários montem times virtuais com os atletas reais do campeonato e compitam em uma liga baseada no desempenho dos jogadores nas partidas.

A aplicação foi construída com Python, utilizando o micro-framework Flask.

---

## Funcionalidades

- **Sistema de Autenticação:** Cadastro e login de usuários.
- **Sistema de Permissões:** Cargos de Administrador, Líder de Delegação e Usuário padrão.
- **Painel de Administração:** Gerenciamento de delegações, partidas, registro de placares e eventos (gols, MVP).
- **Painel de Líder:** Gerenciamento de jogadores (adicionar/remover) da sua própria delegação.
- **Fantasy Game:**
    - Criação de time de fantasia personalizado.
    - Escalação de time (1 goleiro e 4 jogadores de linha) com validação em tempo real para evitar jogadores duplicados.
- **Visualização Pública:**
    - Ranking geral com pontuação calculada automaticamente.
    - Lista de todos os jogadores e páginas de perfil com estatísticas individuais.

---

## Como Rodar o Projeto Localmente

Siga os passos abaixo para configurar e executar a aplicação no seu ambiente de desenvolvimento.

### Pré-requisitos

- Python 3.8 ou superior.
- `pip` (gerenciador de pacotes do Python).

### 1. Criar e Ativar o Ambiente Virtual

Este projeto é projetado para ser executado em um ambiente virtual isolado. Se a pasta `.venv` ainda não existir, crie-a:

```sh
python -m venv .venv
```

Em seguida, ative o ambiente. Este passo é **obrigatório** sempre que você abrir um novo terminal para trabalhar no projeto.

**No Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**No macOS ou Linux:**
```bash
source .venv/bin/activate
```
Após a ativação, você verá `(.venv)` no início do seu prompt de comando.

### 2. Instalar as Dependências

Com o ambiente virtual ativo, instale todas as bibliotecas necessárias que estão listadas no arquivo `requirements.txt`.

```sh
pip install -r requirements.txt
```

### 3. Configurar o Flask

O Flask precisa saber qual é o arquivo principal da aplicação. Defina a variável de ambiente `FLASK_APP`.

**No Windows (PowerShell):**
```powershell
$env:FLASK_APP = "main.py"
```

**No macOS ou Linux:**
```bash
export FLASK_APP=main.py
```

### 4. Criar o Usuário Administrador

Na primeira vez que for executar, você precisará criar um usuário administrador para gerenciar o sistema. Use o comando customizado `create-admin`.

```sh
python -m flask create-admin "Seu Nome" "seu-email@admin.com" "sua-senha-forte"
```
*Substitua os dados pelos que você desejar.*

### 5. Executar a Aplicação

Finalmente, inicie o servidor de desenvolvimento do Flask.

```sh
python -m flask run
```

O servidor estará rodando em `http://127.0.0.1:5000/`. Abra este endereço no seu navegador para acessar a aplicação.
