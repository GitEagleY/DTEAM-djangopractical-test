FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y \
        postgresql-client \
        build-essential \
        libpq-dev \
        gcc 

    

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy project dependencies
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

    
# Copy the entire project
COPY . /app/

RUN poetry run python manage.py makemigrations

# Expose ports
EXPOSE 8000

