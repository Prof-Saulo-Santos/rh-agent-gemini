import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Configurações de Caminho
DATA_DIR = "dados_rh"
FAISS_INDEX_PATH = "faiss_index"


def main():
    print(f"Iniciando a ingestão de múltiplos documentos no diretório: {DATA_DIR}")

    if not os.path.exists(DATA_DIR):
        print(
            f"ERRO: Diretório não encontrado em {DATA_DIR}. Crie a pasta e adicione os documentos."
        )
        return

    # 1. Carregar todos os documentos de texto do diretório
    # Usa o glob '**/*.txt' para buscar qualquer arquivo .txt na pasta dados_rh
    loader = DirectoryLoader(
        DATA_DIR,
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"},
    )

    documents = loader.load()
    print(f"Sucesso! {len(documents)} arquivos de políticas carregados.")

    # Imprime os nomes dos arquivos lidos (útil para debug)
    for doc in documents:
        print(f" - Lendo: {doc.metadata.get('source', 'Desconhecido')}")

    # 2. Dividir os textos em chunks menores
    # Para políticas de RH (textos contínuos e parágrafos), 1000 caracteres é um bom balanço.
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    print(f"Documentos divididos em {len(chunks)} pedaços (chunks).")

    # 3. Criar os Embeddings localmente na CPU
    print("Gerando Embeddings (isso pode levar alguns instantes)...")
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2", model_kwargs={"device": "cpu"}
    )

    # 4. Criar o FAISS Vector Store e Salvar Localmente
    vectorstore = FAISS.from_documents(chunks, embeddings)

    vectorstore.save_local(FAISS_INDEX_PATH)
    print(
        f"\nBanco de dados FAISS gerado e salvo na pasta '{FAISS_INDEX_PATH}' com sucesso!"
    )


if __name__ == "__main__":
    main()
