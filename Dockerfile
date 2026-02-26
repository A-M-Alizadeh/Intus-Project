FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements/base.txt backend/requirements/production.txt /tmp/requirements/
RUN pip install --no-cache-dir -r /tmp/requirements/production.txt

COPY backend /app/backend
RUN chmod +x /app/backend/entrypoint.sh

WORKDIR /app/backend

EXPOSE 7860

ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:7860", "--workers", "2"]
