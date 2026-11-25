FROM python:3.12-slim

# Compilers/interpreters your platform runs: C, C++ and JavaScript
RUN apt-get update && apt-get install -y --no-install-recommends gcc g++ nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Run as a normal user, not root
RUN useradd -m appuser && chown -R appuser /app
USER appuser

ENV PORT=10000
CMD gunicorn app:app --bind 0.0.0.0:${PORT} --workers 2 --timeout 60
