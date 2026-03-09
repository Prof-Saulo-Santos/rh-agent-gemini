🚀 **De RAG Estático a IA com Memória: Os Desafios do Deploy em Nuvem** ☁️

Hoje finalizei um dos projetos mais desafiadores do meu portfólio: o **Agente de RH Corporativo**. Diferente do meu projeto anterior (o *Finance Agent Gemini*), que era um script "Stateless" (sem estado), este novo Agente representa um salto arquitetural na minha jornada como AI Engineer.

🧠 **1. O Grande Diferencial: RAG com Memória Contextual**
O desafio técnico aqui foi evoluir o Retrieval-Augmented Generation (RAG). Usando `LangChain` e `FAISS`, implementei o `RunnableWithMessageHistory`. Agora, o agente não apenas faz busca vetorial em PDFs de RH, mas mantém o contexto da conversa. Se o usuário perguntar *"Quantos dias de férias CLT eu tenho?"* e seguir com *"Posso dividi-las em três?"*, a engine (Gemini 2.5 Flash) entende pronomes e reformula as intenções dinamicamente antes de consultar o banco!

🏗️ **2. A Saga do Deploy: A Parede da AWS**
A arquitetura inicial foi desenhada para a **AWS App Runner**. Containerizei o app com um `Dockerfile` robusto (usando o `uv` para dependências ultrarrápidas), fiz o build de 4.5GB (PyTorch) e o push para o ECR privado. O serviço subiu, o Auto Scaling estava configurado (com custo estimado otimizado de ~$12/mês)... mas a interface travou. 
O Diagnóstico Investigativo? **WebSockets**. A AWS App Runner é fantástica para APIs tradicionais, mas bloqueia nativamente túneis de WebSockets de longa duração, uma tecnologia fundamental para as atualizações em tempo real da casca do Streamlit.

🤗 **3. A Solução Elegante: Hugging Face Spaces**
O bom engenheiro Cloud precisa saber pivotar! Ao invés de lutar contra a rede da AWS subindo instâncias EC2 manuais, migrei toda a operação para o **Hugging Face Spaces** (via Docker SDK). 
O resultado? Sensacional!
* WebSockets 100% suportados nativamente (a UI Streamlit rodou lisa na porta `7860`).
* O banco vetorial FAISS é gerado em tempo de Execução (`CMD`) a cada reinício da máquina via script, garantindo dados sempre frescos no cache da RAM.
* E o melhor: Custo Operacional **Zero**.

🐧 **4. Engenharia de Confiabilidade (Gambiarra DevOps)**
O plano gratuito do Hugging Face Spaces possui um mecanismo de "Sleep" (hibernação) se a aplicação ficar sem tráfego por 48 horas. Para manter meu portfólio sempre acessível para os recrutadores, escalei a automação para minha própria infra local! Configurei um serviço `cron` no meu Linux (`crontab -e`) que realiza um ping em background (`curl -s -f > /dev/null`) todos os dias ao meio-dia. O famoso "Keep-Alive" está vivo e funcional!

A jornada completa da infraestrutura local até a Nuvem foi repleta de aprendizados sobre arquiteturas Serverless, redes stateful e MLOps.

🔗 Confira o código completo no meu GitHub: [Coloque seu link do GitHub aqui]
🌐 Teste o Agente ao vivo (Deploy via Hugging Face): [Coloque seu link do HF aqui]

#InteligenciaArtificial #AI #CloudComputing #AWS #HuggingFace #MachineLearning #Python #DevOps #LangChain #Streamlit #DataScience #MLOps
