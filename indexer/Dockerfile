FROM python:2.7-wheezy

RUN apt-get update && apt-get install -y netcat

RUN mkdir -p /opt/reddyt
WORKDIR /opt/reddyt

COPY deps.txt .
RUN pip install -r ./deps.txt
COPY reddyt.py ./reddyt.py
COPY app.py ./app.py
COPY wait-init.sh ./wait-init.sh
COPY config.json ./config.json

CMD ["python", "app.py"]
