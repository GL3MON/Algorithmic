FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y docker.io && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY . .

VOLUME /var/run/docker.sock

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]