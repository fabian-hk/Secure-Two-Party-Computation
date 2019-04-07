FROM python:3.7-alpine

COPY . /app
WORKDIR /app

RUN pip install protobuf

CMD ["python", "-m", "unittest", "tests/test_circuit.py"]