FROM python:3.12-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el proyecto
COPY . .

# Recoger archivos estáticos
RUN python manage.py collectstatic --noinput --settings=mesamaestra.settings.prod

# Exponer puerto de Gunicorn
EXPOSE 8000

# Comando de arranque
CMD ["gunicorn", "mesamaestra.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]