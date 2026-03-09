---
title: Agente RH
emoji: 👔
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---
# 👔 RH Agent: Assistente RAG com Memória Contextual

![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Interface_Web-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Orquestra%C3%A7%C3%A3o-1C3C3C?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_2.5-LLM_Google-8E75B2?logo=google&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Embeddings-FFD21E?logo=huggingface&logoColor=black)
![FAISS](https://img.shields.io/badge/FAISS-Banco_Vetorial-1082C5)
![Docker](https://img.shields.io/badge/Docker-Conteineriza%C3%A7%C3%A3o-2496ED?logo=docker&logoColor=white)
![AWS App Runner](https://img.shields.io/badge/AWS-App_Runner-232F3E?logo=amazon-aws&logoColor=white)
![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

![Demonstração do Agente RH](image/rh-agent-gemini.jpg)

Um sistema avançado de **Agentic RAG (Retrieval-Augmented Generation)** focado no setor de Recursos Humanos. Este projeto transcende a busca vetorial estática ao incorporar memória conversacional profunda, permitindo interações humanas fluidas e consultas complexas através de múltiplos documentos normativos. Desenvolvido com o ecossistema moderno de IA e orquestrado no AWS App Runner.

## 🎯 Por que este projeto é diferente?

Diferente de sistemas Q&A tradicionais (`Single-turn`), este Agente possui **Estado (History-Aware)**.
Se um funcionário pergunta *"Quantos dias de férias eu tenho?"* e em seguida pergunta *"E posso dividi-las em três?"*, a IA mantém o raciocínio. Ela reformula a intenção da segunda pergunta baseada na primeira (descobrindo silenciosamente que *"las"* refere-se a *"férias"*), pesquisa novamente nos vetores e entrega a resposta corretíssima embasada no documento `politica_ferias.txt`.

## ⚙️ Arquitetura e Stack Tecnológica

O sistema foi arquitetado visando isolamento, rapidez e pronto para escalar na nuvem (Cloud-Native):

- **LLM Core:** Google Gemini 2.5 Flash via `langchain-google-genai`.
- **Orquestração Inteligente (LCEL):** LangChain com `RunnableWithMessageHistory` e `history_aware_retriever`.
- **Motor de Embeddings Local:** `all-MiniLM-L6-v2` via HuggingFace (Open-source, rodando na CPU para custo-zero de vetorização).
- **Vector Database:** FAISS (Facebook AI Similarity Search) para busca semântica em lote (`DirectoryLoader`).
- **Gerenciador de Pacotes Python:** `uv` (Rust-based, ultrarrápido).
- **Interface:** Streamlit com `StreamlitChatMessageHistory` para gerenciar a sessão local do usuário.
- **Deploy/DevOps:** Imagem Docker otimizada (`Dockerfile`) gerenciada via Amazon ECR e hospedada no AWS App Runner (Serverless Container).

## 🚀 Como Executar Localmente

Você precisará de uma chave API do Google AI Studio (`GOOGLE_API_KEY`) no seu arquivo `.env`.

```bash
# 1. Clone o repositório
git clone https://github.com/Prof-Saulo-Santos/rh-agent-gemini.git
cd rh-agent-gemini

# 2. Utilize o UV para sincronizar dependências ultrarrápido
uv sync

# 3. Gere o Banco FAISS ingerindo os documentos da pasta /dados_rh
uv run python src/ingest.py

# 4. Inicie o Servidor Streamlit
uv run streamlit run src/app.py
```

## ☁️ Deploy MLOps na Nuvem (AWS App Runner)

Este repositório está pronto para a nuvem. O `Dockerfile` expõe a porta `8501` e gerencia as dependências "frozen" via `uv`.

1. Autenticação no ECR via AWS CLI.
2. Build e Push da Imagem:
   ```bash
   docker build -t rh-agent-gemini .
   docker tag rh-agent-gemini:latest <id_conta>.dkr.ecr.sa-east-1.amazonaws.com/rh-agent-gemini:latest
   docker push <id_conta>.dkr.ecr.sa-east-1.amazonaws.com/rh-agent-gemini:latest
   ```
3. Anexe o contêiner a um serviço no **AWS App Runner** para obter um link público HTTPS auto-escalável.

---
*Construído como bloco fundacional para Arquitetura de LLMs Multi-Agentes em Projetos de Engenharia de IA.*
