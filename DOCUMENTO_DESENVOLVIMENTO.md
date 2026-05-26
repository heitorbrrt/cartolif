# Documento de Desenvolvimento - JIFBA Fantasy App

## 1. Visão Geral

O projeto consiste em desenvolver um aplicativo de fantasy game, similar ao Cartola FC, para o campeonato escolar JIFBA (Jogos Internos do IFBA - Campus Irecê). O objetivo é aumentar o engajamento dos estudantes com o evento, permitindo que eles criem times virtuais com os jogadores reais das delegações e pontuem de acordo com o desempenho deles nas partidas.

**Tema:** Copa do Mundo 2024

---

## 2. Requisitos Funcionais

### 2.1. Gerenciamento de Usuários
- **Cadastro e Login:** Usuários poderão se cadastrar com e-mail e senha.
- **Perfis de Usuário:** Cada usuário terá um perfil simples com seu nome e time de fantasia.

### 2.2. Sistema de Permissões (Cargos)
O sistema terá três níveis de acesso principais:

- **Administrador (Admin):**
    - Gerencia todas as permissões.
    - Cadastra e edita delegações.
    - Registra os resultados das partidas (placar, gols, etc.).
    - Atribui o prêmio de "Melhor da Partida" a um jogador.
    - Pode moderar conteúdo e usuários.

- **Líder de Delegação:**
    - Cargo atribuído por um Administrador.
    - Pode cadastrar e gerenciar os jogadores da sua própria delegação.

- **Usuário Padrão:**
    - Cria e gerencia seu time de fantasia.
    - Visualiza o ranking geral.
    - Visualiza as estatísticas dos jogadores e das partidas.

### 2.3. Gerenciamento do Time de Fantasia
- **Criação do Time:** Cada usuário pode criar um time de fantasia, dando um nome a ele.
- **Escalação:** O usuário deverá escalar seu time selecionando jogadores reais das delegações, incluindo um goleiro. (Regra a definir: limite de jogadores por delegação, esquema tático, etc.).
- **Mercado:** O "mercado" de jogadores fecha antes do início de cada rodada de jogos para evitar escalações durante as partidas.

### 2.4. Sistema de Pontuação
A pontuação será baseada no desempenho real dos jogadores. Sugestão inicial:
- **Gol Feito:** +8 pontos
- **Melhor da Partida:** +5 pontos
- **Partida sem sofrer gol (Goleiro):** +5 pontos
- **Defesa Difícil (Goleiro):** +2 pontos
- **Gol Sofrido (Goleiro):** -2 pontos

### 2.5. Histórico e Estatísticas
- **Página do Jogador:** Cada jogador real terá uma página com seu histórico:
    - Total de partidas jogadas.
    - Total de gols marcados.
    - Quantidade de vezes que foi "Melhor da Partida".
- **Ranking:** Haverá uma tela de ranking geral mostrando a pontuação de todos os usuários do fantasy game.

---

## 3. Modelo de Dados (Sugestão)

- **Usuario:** `(id, nome, email, senha, cargo)`
- **Delegação:** `(id, nome, id_lider)`
- **JogadorReal:** `(id, nome, id_delegacao)`
- **TimeFantasia:** `(id, nome, id_usuario)`
- **Escalacao:** `(id_time_fantasia, id_jogador_real)`
- **Partida:** `(id, data, delegacao_A, delegacao_B, placar_A, placar_B)`
- **Desempenho:** `(id, id_partida, id_jogador, gols, foi_melhor_da_partida)`

---

## 4. Diretrizes de UI/UX

Conforme solicitado, a interface será limpa e moderna:
- **Estilo "Quadrado":** Uso de cards, botões e layouts baseados em retângulos e quadrados, com cantos pouco ou nada arredondados.
- **Sem Gradientes:** Cores sólidas e chapadas.
- **Hierarquia Visual Clara:** Uso de tipografia (tamanho, peso da fonte) para guiar o usuário.
- **Paleta de Cores:** Paleta limitada e consistente, possivelmente inspirada no tema da Copa do Mundo e na identidade visual do IFBA.
- **Foco no Conteúdo:** Evitar bordas e elementos decorativos desnecessários. A informação é a prioridade.

---

## 5. Arquitetura e Tecnologias (Sugestão)

- **Frontend (Aplicativo):**
    - **Linguagem:** Kotlin
    - **UI:** Jetpack Compose (ideal para criar interfaces declarativas e seguir as diretrizes de UI/UX).
    - **Arquitetura:** MVVM (Model-View-ViewModel).
- **Backend:**
    - **Firebase:** Uma excelente opção para começar rápido.
        - **Authentication:** Para gerenciar login e cadastro.
        - **Firestore:** Como banco de dados NoSQL para armazenar todos os dados (usuários, jogadores, pontuações).
        - **Cloud Functions:** Para lógicas de backend, como calcular as pontuações de uma rodada.

---

## 6. Próximos Passos

1.  **Configuração do Projeto:** Criar o projeto Android Studio com as dependências necessárias (Jetpack Compose, Firebase).
2.  **Autenticação:** Implementar as telas e a lógica de Cadastro e Login.
3.  **Estrutura do Banco de Dados:** Modelar e criar as coleções no Firestore.
4.  **Telas Principais:** Desenvolver as telas para visualização de jogadores, ranking e escalação do time.
5.  **Painel de Admin:** Criar as funcionalidades para os administradores e líderes de delegação.
