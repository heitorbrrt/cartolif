# Changelog - CartolIF

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased] - 2024-07-26

### Added (Adicionado)

- **Planejamento e Estrutura do Projeto**
    - Adicionado `DOCUMENTO_DESENVOLVIMENTO.md` detalhando a visão do projeto, requisitos, stack de tecnologia (Flask, SQLAlchemy, Pico.css), modelo de dados e roadmap de implementação.
    - Criada a estrutura de pacotes da aplicação Flask (`cartolif/`) usando o padrão de *application factory* e *blueprints*.
    - Adicionado `requirements.txt` com as dependências do projeto.
    - Adicionado este arquivo, `CHANGELOG.md`.

- **Fase 1: Fundação e Autenticação**
    - Implementado o modelo de dados `User` com hash de senhas em `models.py`.
    - Configurado o sistema de autenticação com `Flask-Login`.
    - Criado o blueprint `auth` com rotas para cadastro (`/signup`), login (`/login`) e logout (`/logout`).
    - Criados os templates HTML para `base.html`, `login.html` e `signup.html` com estilo minimalista via `Pico.css`.
    - Implementada a lógica completa de registro de novos usuários e login/logout.

- **Fase 2: Painéis de Gerenciamento (Admin e Líder)**
    - Expandido o `models.py` com os modelos `Delegação` e `Jogador`, incluindo os relacionamentos.
    - Criado o blueprint `admin` para funcionalidades administrativas, protegido por um decorator `@admin_required`.
    - Adicionado um comando de terminal (`flask create-admin`) para criar o primeiro usuário administrador.
    - Implementada a interface de gerenciamento de delegações (criar e listar) no painel de admin.
    - Implementada a funcionalidade para o admin designar um usuário como `Líder` de uma delegação.
    - Criado o blueprint `lider` para funcionalidades dos líderes de delegação, protegido por um decorator `@lider_required`.
    - Implementada a interface para líderes adicionarem e visualizarem jogadores de sua própria delegação.
    - Atualizada a barra de navegação principal (`base.html`) para exibir dinamicamente os links para os painéis de Admin e Líder, de acordo com o cargo do usuário logado.
