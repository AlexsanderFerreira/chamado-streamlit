# Usar a imagem oficial do Python como base
FROM python:3.9-slim

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt /app/

# Instalar as dependências do projeto no container
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos os outros arquivos do projeto para o diretório de trabalho no container
COPY . /app/

# Definir a variável de ambiente para o arquivo .env (opcional, se necessário)
# Se você precisa do arquivo .env, o Docker vai já ter copiado o arquivo .env
# Você pode definir variáveis de ambiente específicas aqui também, se necessário
# ENV ENV_PATH="/app/.env"

# Expor a porta que o Streamlit usará
EXPOSE 8501

# Definir o comando para rodar o Streamlit quando o container for iniciado
CMD ["streamlit", "run", "app.py"]
