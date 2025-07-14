# Usar imagem Python oficial
FROM python:3.11-slim

# Definir variáveis de ambiente
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
  poppler-utils \
  file \
  && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar arquivos de dependências
COPY pyproject.toml poetry.lock* ./

# Copiar código da aplicação
COPY . .

# Instalar Poetry
RUN pip install poetry

# Configurar Poetry para não criar ambiente virtual
RUN poetry config virtualenvs.create false

# Instalar dependências
RUN poetry install --only main

# Expor porta
EXPOSE 8000

# Comando padrão
CMD ["poetry", "run", "uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"] 