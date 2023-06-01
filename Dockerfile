FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get -y update
RUN apt-get -y upgrade

RUN apt install build-essential -y

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]