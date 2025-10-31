# Use uma imagem oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta que a aplicação vai usar
EXPOSE 5000

# Define variáveis de ambiente
ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1

# Comando para executar a aplicação
CMD ["python", "run.py"]