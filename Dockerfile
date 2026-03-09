# Usa uma imagem oficial leve do Python 3.13
FROM python:3.13-slim

# Instala o gerenciador de pacotes ultra-rápido 'uv' escrito em Rust
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de gerenciamento de dependências primeiro (Melhora o cache do Docker)
COPY pyproject.toml uv.lock ./

# Instala os pacotes primeiro (usando o uv para velocidade)
RUN uv sync --frozen

# Copia todo o restante do código do projeto para o container
COPY . /app

# Gera o banco de dados vetorial FAISS a partir dos arquivos TXT
RUN uv run python src/ingest.py

# Expõe a porta padrão que o HuggingFace Spaces utiliza (7860)
EXPOSE 7860

# Comando de inicialização do servidor
# Passamos address=0.0.0.0 para que o HuggingFace consiga mapear a porta corretamente para a web
CMD ["uv", "run", "streamlit", "run", "src/app.py", "--server.port=7860", "--server.address=0.0.0.0"]
