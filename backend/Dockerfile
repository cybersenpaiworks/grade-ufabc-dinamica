# backend/Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Impede a criação de arquivos .pyc e força o log em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

EXPOSE 8000

# Executa o Uvicorn apontando para todas as interfaces de rede do container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]