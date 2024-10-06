FROM python:3.12-slim

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet dans le conteneur
COPY . .

# Définir les variables d'environnement pour Flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Lancer l'application Flask
CMD ["flask", "run", "--host=0.0.0.0"]
