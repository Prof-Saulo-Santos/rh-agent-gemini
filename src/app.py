import streamlit as st
import os
from dotenv import load_dotenv, find_dotenv

# LangChain Imports
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.chains import (
    create_history_aware_retriever,
    create_retrieval_chain,
)
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Carrega as variáveis de ambiente (.env)
load_dotenv(find_dotenv())

FAISS_INDEX_PATH = "faiss_index"


# ==========================================
# 1. Configuração do Core de IA (Cache)
# ==========================================
@st.cache_resource(show_spinner="Carregando Inteligência Artificial...")
def get_vectorstore():
    # Inicializa o mesmo modelo de embedding usado no ingest.py
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2", model_kwargs={"device": "cpu"}
    )

    if os.path.exists(FAISS_INDEX_PATH):
        vectorstore = FAISS.load_local(
            FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True
        )
        return vectorstore
    else:
        st.error(
            "Banco FAISS não encontrado. Rode o `uv run python src/ingest.py` primeiro."
        )
        st.stop()
        return None


def init_rag_with_memory():
    # 1. Obter a chave e validar
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        st.error("Chave GOOGLE_API_KEY não encontrada no `.env`.")
        st.stop()

    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 5}
    )  # Para RH, 5 blocos já são suficientes

    # 2. Conectar LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.1,  # Pouca criatividade para não inventar regras do RH
        api_key=api_key,
    )

    # 3. Criar a parte 1 da Memória: O Contextualizador de Perguntas
    # (Pega a pergunta atual + histórico e escreve uma pergunta auto-suficiente para buscar no PDF)
    contextualize_q_system_prompt = """Dado um histórico de chat e a pergunta mais recente do usuário \
    que pode fazer referência ao histórico, formule uma pergunta isolada que possa ser compreendida \
    sem o histórico do chat. NÃO responda à pergunta, apenas reformule-a se necessário, ou retorne-a como está."""

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    # 4. Criar a parte 2: O Respondendor Oficial (Question Answering Chain)
    qa_system_prompt = """Você é um assistente atencioso do Recursos Humanos (RH) da empresa. \
    Use as seguintes peças de contexto recuperadas das políticas internas para responder à pergunta. \
    Se você não sabe a resposta ou as políticas fornecidas não mencionam o assunto, diga educadamente. \
    Não invente regras.

    Contexto recuperado das Políticas:
    {context}"""

    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    # 5. Juntar tudo na Retrieval Chain Final
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain


# ==========================================
# 2. Interface de Chat e Histórico (Streamlit)
# ==========================================
st.set_page_config(
    page_title="Agente de RH com Memória", page_icon="👔", layout="centered"
)
st.title("👔 Agente de RH Corporativo")
st.markdown(
    "Faça qualquer pergunta sobre as nossas políticas de **Férias**, **Código de Conduta** ou **Home Office**."
)

# O LangChain tem uma classe especial só para conversar com o Streamlit:
# Ela amarra o histórico da LLM diretamente ao dicionário interno da tela do Streamlit.
msgs = StreamlitChatMessageHistory(key="langchain_messages")

# Se o histórico estiver vazio, a IA dá as boas vindas.
if len(msgs.messages) == 0:
    msgs.add_ai_message(
        "Olá! Eu sou o assistente virtual do RH. Como posso ajudar você com nossas políticas hoje?"
    )

# Instanciar a cadeia RAG pesada (que nós criamos na função acima)
rag_chain = init_rag_with_memory()

# O GRANDE DIFERENCIAL DO PROJETO: Conectar a RAG Chain ao SessionState History
conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    lambda session_id: msgs,  # A função que provém as mensagens
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)

# Desenha as mensagens do histórico na tela
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# Caixa de input para o usuário
user_input = st.chat_input("Digite sua dúvida pro RH aqui...")

if user_input:
    # Mostra a mensagem do usuário na tela e salva
    st.chat_message("human").write(user_input)

    with st.chat_message("ai"):
        with st.spinner("Buscando nas políticas..."):
            try:
                # Chama a LLM passando a pergunta e um session_id ("rh_chat")
                # A mágica acontece aqui: ela lê a pergunta, junta com o `msgs` do Streamlit,
                # vai no Vector Database, e gera a resposta contextualizada sozinha!
                response = conversational_rag_chain.invoke(
                    {"input": user_input},
                    config={"configurable": {"session_id": "rh_chat"}},
                )

                answer = response["answer"]
                st.write(answer)

                # Bônus: Mostrar as fontes de onde as regras foram tiradas!
                with st.expander("Ver Documentos Fonte"):
                    sources = [
                        doc.metadata.get("source", "") for doc in response["context"]
                    ]
                    # Set para remover fontes repetidas
                    for src in set(sources):
                        st.info(f"📄 Arquivo: `{src}`")

            except Exception as e:
                st.error(f"Erro ao processar: {e}")
