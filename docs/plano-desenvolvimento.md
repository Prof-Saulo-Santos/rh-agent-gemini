# Plano de Desenvolvimento: Agente de RH com Memória

Este plano detalha as etapas de construção do nosso primeiro projeto avançado. A transição do `finance-rag` (1 PDF, Sem Memória) para este projeto (Vários PDFs, Com Memória) é o degrau ideal de aprendizado para iniciar o portfólio de Agentes Inteligentes.

## Fases do Projeto (Duração Estimada: 1 Dia de Estudo Prático)

### Tarefa 1: Setup do Ambiente e Base de Documentos
- [ ] Inicializar o projeto usando `uv init` na pasta do projeto.
- [ ] Instalar as dependências via `uv` (Streamlit, LangChain, LangChain-Google-GenAI, FAISS, PyPDF).
- [ ] Criar e configurar o arquivo `.env` para a `GOOGLE_API_KEY`.
- [ ] Gerar 3 a 5 "Documentos Fictícios de RH" (em PDF ou TXT) abordando regras de férias, dress code e política de horas extras.
- [ ] Salvar os documentos em um diretório `dados_rh/`.

### Tarefa 2: Ingestão de Lote (Multi-Document Retrieval)
- [ ] Criar script `ingest.py`.
- [ ] Desenvolver a lógica para iterar e ler todos os arquivos simultaneamente da pasta `dados_rh/`.
- [ ] Otimizar o Chunking (Tamanho de pedaços) para capturar o contexto de múltiplos documentos mantendo os metadados (nome de qual arquivo a informação veio).
- [ ] Gerar o VectorDatabase (FAISS) usando embeddings locais (via HuggingFace ou outra técnica econômica) e salvar em `faiss_index/`.

### Tarefa 3: Construção do Core RAG com Memória
- [ ] Criar script `app.py` (ou `agent.py`).
- [ ] Carregar o Vector Database e configurar o Retriever.
- [ ] Integrar a LLM do Google Gemini (ex: `gemini-2.5-flash`).
- [ ] **O Grande Diferencial:** Implementar a `ConversationBufferMemory` ou `RunnableWithMessageHistory` do LangChain. O sistema precisará reter um histórico da conversa para realizar buscas vetoriais baseadas não só na última pergunta, mas no contexto geral (ex: "E nos feriados?" deve ser entendido como "Como funcionam as horas extras em feriados?").

### Tarefa 4: Interface do Usuário (Streamlit)
- [ ] Construir o layout tipo chat no Streamlit.
- [ ] Ligar a UI com o LLM (Chain), assegurando que o Session State guarde ativamente a lista (lista de mensagens) processável para a cadeia de raciocínio.
- [ ] Mostrar visualmente na interface qual documento foi utilizado para a resposta (ex: Fonte: "Politica_de_Ferias.pdf").

### Tarefa 5: Testes Práticos e Refinamentos
- [x] Perguntar sobre uma regra específica.
- [x] Fazer uma pergunta consequente omitindo o sujeito para testar a memória.
- [ ] Adicionar um `.pre-commit-config.yaml` básico e um `.gitignore` para a segurança no GitHub.
- [ ] Produzir o README.md final deste projeto para o portfólio.

### Tarefa 6: Implantação na Nuvem (AWS App Runner)
- [ ] Criar o `Dockerfile` otimizado para a aplicação Streamlit com FAISS.
- [ ] Construir a imagem Docker localmente para testes.
- [ ] Subir a imagem para o Amazon Elastic Container Registry (ECR).
- [ ] Criar e configurar o serviço no AWS App Runner apontando para a imagem do ECR, passando as variáveis de ambiente necessárias (`GOOGLE_API_KEY`).
- [ ] Validar a aplicação no domínio público gerado pelo App Runner.
