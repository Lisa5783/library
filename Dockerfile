FROM python:3.11-slim
LABEL maintainer="saeveranna@gmail.com"
LABEL description="Flask application container"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
RUN adduser --disabled-password --gecos '' appuser && chown -R appuser:appuser /app
USER appuser
EXPOSE 5000
ENV PYTHONUNBUFFERED=1 FLASK_ENV=production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "run:app"]
