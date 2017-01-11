FROM python:3.4-alpine
RUN mkdir -p /opt/reddyt
COPY deps.txt /opt/reddyt/deps.txt
COPY app.py /opt/reddyt/app.py
WORKDIR /opt/reddyt
RUN pip install -r deps.txt
CMD ["python", "app.py"]
