# Changelog - CartolIF

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2024-07-26

### Added (Adicionado)

- **Planejamento e Estrutura do Projeto**
    - Adicionado `DOCUMENTO_DESENVOLVIMENTO.md` e `README.md`.
    - Criada a estrutura de pacotes da aplicação Flask (`cartolif/`) com *application factory* e *blueprints*.
    - Adicionado `requirements.txt` com as dependências do projeto.

- **Funcionalidades Principais (Fases 1-5)**
    - **Autenticação:** Sistema completo de cadastro, login e logout de usuários.
    - **Permissões:** Cargos de `ADMIN`, `LIDER` e `USER` com rotas protegidas.
    - **Painel de Admin:** Gerenciamento de delegações, partidas, placares e registro de eventos (Gols, MVP).
    - **Painel de Líder:** Gerenciamento de jogadores da própria delegação, incluindo nome e posição.
    - **Fantasy Game:** Criação de time e interface de escalação de jogadores (1 goleiro, 4 de linha).
    - **Visualização:** Páginas públicas para Ranking geral e perfis de estatísticas de jogadores.
    - **Comandos:** Adicionado comando `flask create-admin` para setup inicial.

### Changed (Alterado)

- **UI/UX (CSS & JavaScript)**
    - Adicionado `custom.css` com uma paleta de cores personalizada (tons de verde do IFBA) para melhorar a identidade visual.
    - Melhorado o estilo da barra de navegação, botões e cards de estatísticas.
    - Adicionado `main.js` com lógica para impedir a seleção de jogadores duplicados no formulário de escalação, melhorando a experiência do usuário.
    - Templates `base.html` e `perfil_jogador.html` atualizados para carregar os novos assets e aplicar as novas classes de estilo.

### Fixed (Corrigido)

- Corrigido erro "Internal Server Error" na página de administração.
- Corrigido erro "Not Found" na página inicial.
- Corrigida a herança de template na `index.html` para exibir o layout completo.
