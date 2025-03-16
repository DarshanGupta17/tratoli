# Use official Python image as base
FROM python:3.11

# Set working directory inside container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y netcat && apt-get clean

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose ports (Django: 8000, Daphne: 3001)
EXPOSE 8000 3001

# Default command for running Django + Daphne
CMD ["sh", "-c", "python manage.py migrate && daphne -b 0.0.0.0 -p 3001 TMS.asgi:application & python manage.py runserver 0.0.0.0:8000"]
