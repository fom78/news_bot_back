# Etapa 1: build
FROM python:3.11-slim AS builder

WORKDIR /app

# Instalar dependencias para compilación y SQLite
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependencias
COPY requirements.txt .

# Crear entorno virtual e instalar dependencias
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Etapa 2: runtime
FROM python:3.11-slim AS runtime

# Crear usuario seguro
RUN useradd -m appuser

WORKDIR /app

# Copiar entorno virtual y código fuente
COPY --from=builder /opt/venv /opt/venv
COPY . .

# Configurar entorno virtual por defecto
ENV PATH="/opt/venv/bin:$PATH"

# Variables de entorno de Flask
ENV FLASK_APP=app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
ENV FLASK_ENV=production

# Copiar archivos de entorno (opcional)
COPY .env .env
COPY .flaskenv .flaskenv

# Asignar permisos al usuario no root
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 8080

# Comando de arranque con flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
