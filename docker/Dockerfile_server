FROM python:3.7-alpine

RUN	pip3 install --trusted-host pypi.python.org protobuf

WORKDIR /docker

COPY . /docker

EXPOSE 8448
EXPOSE 8449


CMD ["python3", "Server.py"]
