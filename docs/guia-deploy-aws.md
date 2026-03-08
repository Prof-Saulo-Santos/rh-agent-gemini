# Guia de Implantação: AWS App Runner + Amazon ECR

O nosso `Dockerfile` já está criado e configurado para rodar a aplicação Streamlit empacotando o `uv` e o banco FAISS junto!
Como o seu ambiente local (Ubuntu) não possui o Docker instalado, a melhor forma de fazer o deploy na AWS é enviando o seu código para um repositório no GitHub ou utilizando o protocolo do AWS CLI.

Aqui estão os 3 passos práticos para colocar o projeto no ar.

---

## Passo 1: Criar o Repositório no Amazon ECR
O ECR (Elastic Container Registry) é o "GitHub de Imagens Docker" da AWS.

1. Faça login na sua conta da AWS.
2. Busque por **ECR (Elastic Container Registry)**.
3. Clique em **Criar repositório**.
4. Defina a visibilidade como **Privado** (para proteger seu `.env` e FAISS).
5. Nome do repositório: `rh-agent-gemini`.
6. Clique em **Criar**.

---

## Passo 2: Fazer o Push da Imagem para a AWS
O jeito mais fácil de fazer isso se você não tem o Docker instalado na sua própria máquina de casa é abrir o **AWS CloudShell** (Aquele terminalzinho preto nativo que fica na barra superior direita do console da AWS). Ele já tem Docker e AWS CLI pré-instalados!

No AWS CloudShell, você vai clonar o seu projeto do seu Github e seguir os comandos "Push Commands" (Comandos de push) que o próprio ECR te fornece ao clicar no botão "Exibir comandos de push" dentro do repositório que você criou.

A sequência é:
```bash
# Entrar no AWS CloudShell, clonar seu repositório do github
git clone https://github.com/Prof-Saulo-Santos/rh-agent-gemini.git
cd rh-agent-gemini

# 1. Autenticar o Docker no ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin SEU_ID_AWS.dkr.ecr.us-east-1.amazonaws.com

# 2. Fazer a Build da Imagem de acordo com nosso Dockerfile
docker build -t rh-agent-gemini .

# 3. Aplicar a Tag
docker tag rh-agent-gemini:latest SEU_ID_AWS.dkr.ecr.us-east-1.amazonaws.com/rh-agent-gemini:latest

# 4. Enviar a imagem para a Nuvem
docker push SEU_ID_AWS.dkr.ecr.us-east-1.amazonaws.com/rh-agent-gemini:latest
```

---

## Passo 3: Criar o Serviço no App Runner
Esta é a última etapa. O App Runner vai pegar a imagem que chegou no ECR e transformá-la num link da web público.

1. Busque pelo serviço **AWS App Runner** no console.
2. Clique em **Criar serviço App Runner**.
3. Em *Origem*: Selecione **Container registry** > **Amazon ECR**.
4. Procure a imagem que você acabou de dar push (`rh-agent-gemini:latest`).
5. **CRÍTICO:** Na tela de configurações (Configuração do serviço), vá na seção *Variáveis de ambiente* e adicione obrigatoriamente a sua chave:
   * **Chave:** `GOOGLE_API_KEY`
   * **Valor:** `AIzaSyD4y...` (A sua chave real do Gemini).
6. **Porta:** Certifique-se de preencher a Porta com `8501` (que é a porta do Streamlit exposta no `Dockerfile`).
7. Clique em **Criar e implantar**.

Aguarde cerca de 5 minutos, e a AWS irá retornar um link público seguro (HTTPS) onde qualquer pessoa com o link poderá abrir no celular ou computador e falar de imediato com o seu agente conversacional das políticas de RH!
