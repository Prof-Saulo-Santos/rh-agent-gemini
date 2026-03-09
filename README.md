# 👔 RH Agent: Assistente RAG com Memória Contextual

**🚀 Aplicação ao Vivo:** [Teste o Agente no Hugging Face Spaces](https://huggingface.co/spaces/Prof-Saulo-Santos/agente-rh-gemini)

![Python](https://img.shields.io/badge/Python-3.13%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Interface_Web-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Orquestra%C3%A7%C3%A3o-1C3C3C?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_2.5-LLM_Google-8E75B2?logo=google&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Embeddings-FFD21E?logo=huggingface&logoColor=black)
![FAISS](https://img.shields.io/badge/FAISS-Banco_Vetorial-1082C5)
![Docker](https://img.shields.io/badge/Docker-Conteineriza%C3%A7%C3%A3o-2496ED?logo=docker&logoColor=white)
![Hugging Face Spaces](https://img.shields.io/badge/Hugging%20Face-Spaces-FFD21E?logo=huggingface&logoColor=black)
![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)

![Demonstração do Agente RH](image/rh-agent-gemini.jpg)

Um sistema avançado de **Agentic RAG (Retrieval-Augmented Generation)** focado no setor de Recursos Humanos. Este projeto transcende a busca vetorial estática ao incorporar memória conversacional profunda, permitindo interações humanas fluidas e consultas complexas através de múltiplos documentos normativos. Desenvolvido com o ecossistema moderno de IA e hospedado no Hugging Face Spaces.

## 🎯 Por que este projeto é diferente?

Diferente de sistemas Q&A tradicionais (`Single-turn`), este Agente possui **Estado (History-Aware)**.
Se um funcionário pergunta *"Quantos dias de férias eu tenho?"* e em seguida pergunta *"E posso dividi-las em três?"*, a IA mantém o raciocínio. Ela reformula a intenção da segunda pergunta baseada na primeira (descobrindo silenciosamente que *"las"* refere-se a *"férias"*), pesquisa novamente nos vetores e entrega a resposta corretíssima embasada no documento `politica_ferias.txt`.

## ⚙️ Arquitetura e Stack Tecnológica

O sistema foi arquitetado visando isolamento, rapidez e pronto para escalar na nuvem (Cloud-Native):

- **LLM Core:** Google Gemini 2.5 Flash via `langchain-google-genai`.
- **Orquestração Inteligente (LCEL):** LangChain com `RunnableWithMessageHistory` e `history_aware_retriever`.
- **Motor de Embeddings Local:** `all-MiniLM-L6-v2` via HuggingFace (Open-source, rodando na CPU para custo-zero de vetorização).
- **Vector Database:** FAISS (Facebook AI Similarity Search) gerado em tempo de execução no deploy.
- **Gerenciador de Pacotes Python:** `uv` (Rust-based, ultrarrápido).
- **Interface:** Streamlit com `StreamlitChatMessageHistory` para gerenciar a sessão local do usuário.
- **Deploy/DevOps:** Imagem Docker otimizada (`Dockerfile`) e hospedada nativamente no Hugging Face Spaces com suporte a WebSockets.

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

## ☁️ Deploy MLOps na Nuvem (Hugging Face Spaces)

Este repositório está perfeitamente ajustado para o Hugging Face Spaces. O `Dockerfile` expõe a porta `7860` e gera o banco **FAISS** em tempo de execução (`cmd`) para garantir acesso aos documentos mais recentes.

1. Crie um "New Space" no [Hugging Face](https://huggingface.co/spaces) escolhendo **Docker** e o template **Streamlit**.
2. Nas configurações do seu Space, adicione um Secret chamado `GOOGLE_API_KEY`.
3. Adicione o seu Space como *remote* git no seu terminal local e suba o código:
   ```bash
   git remote add huggingface https://SEU_USUARIO:SEU_TOKEN@huggingface.co/spaces/SEU_USUARIO/nome-do-space
   git push --force huggingface main
   ```
4. A plataforma realizará o Build da imagem Docker (instalando as dependências `uv`) e disponibilizará a URL pública instantaneamente e com suporte nativo a WebSockets!

---
*Construído como bloco fundacional para Arquitetura de LLMs Multi-Agentes em Projetos de Engenharia de IA.*
