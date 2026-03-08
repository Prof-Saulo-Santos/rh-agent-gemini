# Ideia Inicial: Agente de RH com Memória (Chatbot Multi-Documento)

## 🎯 O Problema
O RAG financeiro que fizemos responde uma pergunta e "esquece", e só lê um arquivo por vez. Empresas precisam de agentes que consultem dezenas de documentos (políticas de férias, TI, conduta) e mantenham o contexto da conversa.

## 🚀 O Projeto
Um assistente para funcionários (RH) ou suporte jurídico que lê uma *pasta inteira* com dezenas de PDFs de políticas da empresa.

## 🧠 O Diferencial Técnico para o Portfólio
*   **Memória de Conversação:** O usuário pode perguntar "Quantos dias de férias eu tenho?", o robô responde "30", e o usuário pergunta "E posso dividi-las em 3 vezes?", e o robô **lembra** do contexto da conversa anterior usando `ConversationBufferMemory` ou `RunnableWithMessageHistory`.
*   **Ingestão em Massa:** Processar múltiplos PDFs de um diretório.
*   **Roteamento (Routing):** Opcionalmente, o sistema decide automaticamente em qual grupo de documentos buscar a resposta dependendo da intenção da pergunta.

## 🛠️ Stack Sugerida
*   **Python:** Gerenciado com `uv`
*   **Interface:** Streamlit
*   **Orquestração:** LangChain
*   **Vector Store:** FAISS ou ChromaDB
*   **LLM:** Google Gemini 2.5 Flash

## 📝 Próximos Passos
1. Coletar ou criar 3-5 PDFs de exemplo (políticas fictícias de RH).
2. Inicializar o projeto com `uv init`.
3. Criar pipeline de ingestão para ler a pasta toda.
4. Implementar o LangChain com suporte a sessão/histórico no Streamlit.
