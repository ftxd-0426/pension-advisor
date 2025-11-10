FROM python:3.13-slim
LABEL "language"="python"
LABEL "framework"="flask"

WORKDIR /app

COPY . .

RUN mkdir -p templates && mv index.html templates/index.html || true

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
