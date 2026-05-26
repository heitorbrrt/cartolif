# Documento de Desenvolvimento - CartolIF

## 1. Visão Geral

O projeto **CartolIF** é um aplicativo web de *fantasy game* desenhado especificamente para os Jogos Internos do IFBA - Campus Irecê (JIFBA). A plataforma permitirá que a comunidade acadêmica (alunos e servidores) monte seus próprios times com os atletas que participarão do campeonato, competindo em uma liga virtual baseada no desempenho real dos atletas nas partidas.

O objetivo principal é aumentar o engajamento e a interação da comunidade com o evento esportivo, trazendo uma camada de gamificação e competição saudável.

---

## 2. Requisitos Funcionais Detalhados

### 2.1. Autenticação e Gerenciamento de Usuários
- **RF01: Cadastro de Usuário:** Qualquer pessoa com um e-mail válido poderá se cadastrar fornecendo nome, e-mail e senha.
- **RF02: Login de Usuário:** Usuários cadastrados poderão acessar a plataforma usando e-mail e senha.
- **RF03: Sistema de Permissões (Cargos):** O sistema terá três níveis de acesso:
    - **Administrador:** Controle total sobre a plataforma. Pode gerenciar usuários, delegações, partidas e registrar todos os eventos.
    - **Líder de Delegação:** Gerencia os jogadores de sua própria delegação. Permissão concedida por um Administrador.
    - **Usuário Padrão:** Acesso padrão para montar seu time, visualizar rankings e estatísticas.

### 2.2. Gerenciamento do Campeonato (Admin e Líderes)
- **RF04: Gerenciamento de Delegações (Admin):** O admin poderá criar, editar e excluir delegações (times do campeonato).
- **RF05: Gerenciamento de Jogadores (Líder):** O líder de uma delegação poderá cadastrar, editar e remover os jogadores do seu time.
- **RF06: Gerenciamento de Partidas (Admin):** O admin poderá agendar as partidas, informando as delegações envolvidas e a data/hora.
- **RF07: Registro de Resultados (Admin):** Após uma partida, o admin registrará o placar final e os eventos que geram pontuação.

### 2.3. Funcionalidades do Fantasy Game (Usuário Padrão)
- **RF08: Criação de Time de Fantasia:** Cada usuário poderá criar um time de fantasia, definindo um nome único para ele.
- **RF09: Escalação de Jogadores:** O usuário escalará seu time com 1 Goleiro e 4 jogadores de linha, com um limite a ser definido de jogadores da mesma delegação.
- **RF10: Mercado:** A escalação de times será bloqueada um pouco antes do início de cada rodada de jogos para garantir a integridade da competição.
- **RF11: Visualização de Ranking:** Uma página exibirá o ranking geral dos usuários, ordenado pela pontuação total.
- **RF12: Histórico de Jogador:** Uma página dedicada para cada jogador real, mostrando seu histórico de gols e prêmios de "Melhor da Partida".

### 2.4. Sistema de Pontuação
A pontuação será calculada com base nos eventos registrados pelo Administrador.
- **Gol Feito:** +8 pontos
- **Prêmio "Melhor da Partida":** +5 pontos
- **Partida sem sofrer gol (apenas para o Goleiro):** +5 pontos (Concedido se o time adversário não marcou gols na partida).

---

## 3. Arquitetura e Tecnologias (O "Como")

Para garantir um desenvolvimento ágil e um produto final robusto, a seguinte stack de tecnologia será utilizada:

- **Tipo de Aplicação:** Aplicação Web Responsiva (Mobile-First), renderizada no servidor. Isso garante acesso universal por meio de qualquer navegador em desktops ou celulares sem a necessidade de instalar um aplicativo.

- **Backend:**
    - **Linguagem:** **Python 3**
    - **Framework:** **Flask**. É um micro-framework leve, ideal para prototipagem rápida e projetos de escopo bem definido. Sua simplicidade nos permite focar na lógica de negócio.
    - **Banco de Dados:** **PostgreSQL**. Um sistema de banco de dados relacional robusto e escalável. Para o ambiente de desenvolvimento, usaremos **SQLite** para simplificar a configuração inicial.
    - **ORM (Mapeamento Objeto-Relacional):** **SQLAlchemy** com a extensão **Flask-SQLAlchemy**. Abstrai a comunicação com o banco de dados, permitindo-nos escrever a lógica em Python puro e trocar de SGBD (SQLite para PostgreSQL) com o mínimo de esforço.
    - **Gerenciamento de Sessão:** **Flask-Login** para controlar a autenticação e as sessões de usuário de forma segura.
    - **Segurança:** As senhas serão armazenadas de forma segura usando hashes gerados pela biblioteca **Werkzeug**, que já vem com o Flask.

- **Frontend:**
    - **Estrutura:** **HTML5** renderizado pelo motor de templates **Jinja2**, nativo do Flask.
    - **Estilização:** **Pico.css**. Um framework CSS minimalista que oferece um design limpo, moderno e "quadrado" (como solicitado) com o mínimo de classes e customização, focando na semântica do HTML.
    - **Interatividade:** **JavaScript (Vanilla JS)**. Será usado de forma pontual para melhorar a experiência do usuário (ex: validações de formulário em tempo real), sem a complexidade de frameworks como React ou Vue.

- **Hospedagem (Deployment):**
    - **Plataforma Sugerida:** **PythonAnywhere** ou **Heroku**. Ambas oferecem um plano gratuito ou de baixo custo, ideal para projetos de estudantes, e simplificam o processo de deploy de aplicações Flask.

---

## 4. Modelo de Dados (Estrutura do Banco)

```
// Tabela de Usuários
Usuario {
  id (PK)
  nome (String)
  email (String, Unique)
  password_hash (String)
  cargo (Enum: 'ADMIN', 'LIDER', 'USER')
}

// Tabela de Delegações (Times Reais)
Delegação {
  id (PK)
  nome (String, Unique)
  lider_id (FK -> Usuario.id, Nullable)
}

// Tabela de Jogadores Reais
Jogador {
  id (PK)
  nome (String)
  delegacao_id (FK -> Delegação.id)
}

// Tabela dos Times de Fantasia dos Usuários
TimeFantasia {
  id (PK)
  nome (String)
  usuario_id (FK -> Usuario.id, Unique) // Um time por usuário
}

// Tabela de Associação para Escalação (Muitos-para-Muitos)
Escalacao {
  time_fantasia_id (FK -> TimeFantasia.id)
  jogador_id (FK -> Jogador.id)
  PRIMARY KEY (time_fantasia_id, jogador_id)
}

// Tabela de Partidas Reais
Partida {
  id (PK)
  data (DateTime)
  delegacao_a_id (FK -> Delegação.id)
  delegacao_b_id (FK -> Delegação.id)
  placar_a (Integer)
  placar_b (Integer)
  finalizada (Boolean, default=False)
}

// Tabela para registrar eventos que geram pontos
Evento {
  id (PK)
  partida_id (FK -> Partida.id)
  jogador_id (FK -> Jogador.id)
  tipo_evento (Enum: 'GOL', 'MELHOR_DA_PARTIDA')
}
```

---

## 5. Plano de Implementação (Roadmap)

O desenvolvimento será dividido em fases para uma entrega incremental e organizada.

- **Fase 1: Fundação e Autenticação**
    1. Configurar o projeto Flask, banco de dados com SQLAlchemy.
    2. Criar o modelo de dados `Usuario`.
    3. Implementar as rotas e templates para Cadastro, Login e Logout.
    4. Proteger rotas que exigem autenticação.

- **Fase 2: Painéis de Gerenciamento (Admin e Líder)**
    1. Criar as interfaces de administração.
    2. Implementar o CRUD (Criar, Ler, Atualizar, Deletar) para `Delegação` (Admin).
    3. Implementar o CRUD para `Jogador` (Líder de Delegação, restrito à sua delegação).
    4. Implementar a funcionalidade para o Admin designar um `Líder`.

- **Fase 3: Funcionalidade Central do Usuário**
    1. Implementar a criação do `TimeFantasia`.
    2. Desenvolver a interface de escalação de jogadores, buscando da lista geral.
    3. Criar a página de visualização do próprio time.

- **Fase 4: Lógica do Jogo e Pontuação**
    1. Implementar o CRUD para `Partida` (Admin).
    2. Implementar a interface para o Admin registrar `Eventos` (gols, melhor da partida) pós-jogo.
    3. Desenvolver o script que calcula a pontuação de cada `TimeFantasia` com base nos eventos e atualiza o ranking.

- **Fase 5: Visualização e Finalização**
    1. Criar a página de Ranking Geral.
    2. Criar a página de perfil público para cada `Jogador`, com suas estatísticas.
    3. Polir a interface do usuário e realizar testes de usabilidade.
```