FROM python:3.11.0a6-alpine3.15

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt --no-cache-dir

COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]