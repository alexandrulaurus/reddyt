FROM python:3.4-alpine
RUN mkdir -p /opt/reddyt
COPY deps.txt /opt/reddyt/deps.txt
WORKDIR /opt/reddyt
RUN pip install -r deps.txt
COPY app.py /opt/reddyt/app.py
CMD ["python", "app.py"]
