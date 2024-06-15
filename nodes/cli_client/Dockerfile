FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN apt update && apt install -y git

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "main.py"]