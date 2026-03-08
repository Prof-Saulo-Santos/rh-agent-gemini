# Usa uma imagem oficial leve do Python 3.13
FROM python:3.13-slim

# Instala o gerenciador de pacotes ultra-rápido 'uv' escrito em Rust
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de gerenciamento de dependências primeiro (Melhora o cache do Docker)
COPY pyproject.toml uv.lock ./

# Instala as dependências usando o uv
# O --frozen garante que ele usará exatamente as versões do uv.lock
RUN uv sync --frozen --no-dev

# Copia todo o restante do código do projeto para o container
COPY . /app

# Expõe a porta padrão que o HuggingFace Spaces utiliza (7860)
EXPOSE 7860

# Comando de inicialização do servidor
# Passamos address=0.0.0.0 para que o HuggingFace consiga mapear a porta corretamente para a web
CMD ["uv", "run", "streamlit", "run", "src/app.py", "--server.port=7860", "--server.address=0.0.0.0"]
