# Assistente de IA Avançado para WhatsApp

## 📖 Sobre o Projeto

Este projeto implementa um assistente de IA conversacional avançado e humanizado para interação via WhatsApp. Construído em Python com FastAPI, o assistente utiliza o framework **Agno** e o poder do **Google Gemini** para ir além de um simples chatbot, incorporando funcionalidades de memória persistente e a capacidade de consultar documentos específicos (RAG).

O foco principal foi criar uma experiência de usuário natural e fluida, simulando uma conversa humana através de técnicas como buffering de mensagens e envio de respostas parceladas.

---

## ✨ Principais Funcionalidades

-   🧠 **Memória Conversacional Persistente:** Utiliza **Redis** (ou opcionalmente arquivos locais) para lembrar o contexto de conversas anteriores, permitindo um diálogo contínuo e coerente com cada usuário.
-   📚 **Busca Aumentada por Recuperação (RAG):** O assistente é capaz de consultar uma base de conhecimento própria (neste caso, um documento PDF vetorizado com **ChromaDB**) para responder a perguntas específicas com base em fatos.
-   🗣️ **Interação Humanizada:**
    -   **Buffering de Entrada:** Agrupa mensagens enviadas rapidamente pelo usuário antes de processar, esperando que ele termine de "digitar".
    -   **Respostas Parceladas:** Envia respostas longas em várias mensagens curtas, com pausas, para simular uma digitação natural.
-   🛠️ **Arquitetura Baseada em Agentes e Ferramentas:** Usa uma arquitetura moderna onde o agente de IA pode decidir autonomamente quando usar "ferramentas" (como a busca em documentos) para melhor formular suas respostas.
-   🚀 **Backend Assíncrono:** Construído com **FastAPI**, garantindo alta performance e a capacidade de lidar com múltiplas requisições simultâneas de forma eficiente.

---

## 🏗️ Arquitetura do Projeto

O fluxo de uma mensagem através do sistema é o seguinte:

1.  **WhatsApp** → O usuário envia uma mensagem.
2.  **Evolution API** → A mensagem é recebida e encaminhada via Webhook.
3.  **FastAPI Endpoint** → Nosso backend recebe a requisição.
4.  **Buffering (Redis)** → A mensagem é adicionada a um buffer. Uma tarefa em segundo plano aguarda para ver se mais mensagens chegam.
5.  **Agno Agent** → Após a espera, a mensagem (ou o conjunto de mensagens) é enviada para o agente principal.
6.  **Decisão do Agente:**
    -   Se for uma pergunta geral, ele usa a **Memória Conversacional** (Redis ou Arquivos) para obter o histórico e gerar uma resposta.
    -   Se for uma pergunta sobre o documento, ele ativa a **Ferramenta de RAG** para buscar o contexto relevante no **ChromaDB**.
7.  **LLM (Google Gemini)** → O agente envia o prompt final (com contexto do RAG ou da memória) para o Gemini.
8.  **Resposta Parcelada** → A resposta gerada é quebrada em partes e enviada de volta ao usuário via **Evolution API**, simulando uma digitação natural.

---

## 🛠️ Tecnologias Utilizadas

-   **Backend:** Python 3.11+
-   **Framework Web:** FastAPI
-   **Framework de IA:** Agno
-   **Bibliotecas de IA:** LangChain
-   **LLM:** Google Gemini (1.5 Flash)
-   **Memória e Cache:** Redis
-   **RAG / Vector Store:** ChromaDB
-   **API WhatsApp:** Evolution API
-   **Ambiente de Desenvolvimento:** Docker

---

## ⚙️ Configuração e Instalação

Siga os passos abaixo para configurar e rodar o projeto localmente.

### Pré-requisitos

-   Python 3.11 ou superior
-   Git
-   Docker e Docker Desktop (para rodar o Redis localmente)
-   Uma instância da [Evolution API](https://doc.evolution-api.com/v1/pt/get-started/introduction) configurada e rodando.
-   Acesso à API do Google Gemini.

### Passos de Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/Leozs00/agno_assistant.git](https://github.com/Leozs00/agno_assistant.git)
    cd agno_assistant
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate

    # Linux / macOS
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    -   Renomeie o arquivo `.env.example` para `.env` (se houver um no repositório) ou crie um novo.
    -   Abra o arquivo `.env` e preencha todas as variáveis com suas chaves e credenciais (Google API Key, Evolution API, Redis, etc.).

5.  **Prepare a Base de Conhecimento (RAG):**
    -   Crie uma pasta chamada `data` na raiz do projeto.
    -   Coloque o documento PDF que você deseja usar como base de conhecimento dentro da pasta `data`.
    -   Renomeie o arquivo para `documento_de_conhecimento.pdf` (ou altere o caminho no arquivo `src/rag/ingest.py`).
    -   Execute o script de ingestão para criar o banco de dados de vetores:
        ```bash
        python -m src.rag.ingest
        ```
    -   Isso criará uma pasta `vector_store/` com os dados vetorizados.

### Executando a Aplicação

1.  **Inicie o Redis com Docker:**
    ```bash
    docker start meu-redis-local
    ```
    *(Se for a primeira vez, use o comando `docker run -d --name meu-redis-local -p 6379:6379 redis`)*

2.  **Inicie o servidor FastAPI:**
    ```bash
    uvicorn src.main:app --reload
    ```
    O servidor estará rodando em `http://localhost:8000`.

3.  **Exponha seu servidor com ngrok:**
    Para que a Evolution API possa enviar webhooks para sua máquina local, use o ngrok.
    ```bash
    ngrok http 8000
    ```
    Copie a URL `https://...` gerada e configure-a como a URL de webhook na sua instância da Evolution API (não se esqueça de adicionar `/webhook` ao final).

---

## 🔗 Links de Referência

-   [Documentação do Agno Framework](https://docs.agno.com/)
-   [Documentação da Evolution API](https://doc.evolution-api.com/)
-   [Documentação do LangChain](https://python.langchain.com/)
-   [Google AI for Developers (Gemini)](https://ai.google.dev/)

---

## 👨‍💻 Autor

-   **Leonardo** - [GitHub](https://github.com/Leozs00)
