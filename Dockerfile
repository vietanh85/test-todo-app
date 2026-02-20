FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the database file can be written to
RUN touch todos.db && chmod 666 todos.db

EXPOSE 8000

ENV PORT=8000
ENV HOST=0.0.0.0

CMD ["python", "main.py"]
