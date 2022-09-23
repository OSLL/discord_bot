FROM python:3.8-slim-buster

WORKDIR /bot

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . . 

CMD ["python", "./bot/main.py"]