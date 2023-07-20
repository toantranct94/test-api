FROM python:3.10.0-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Install Redis and RabbitMQ dependencies
RUN apt-get update && apt-get install -y rabbitmq-server redis-server

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./cache /code/cache

RUN mv /code/cache/main.py /code/
# RUN python consume.py

CMD ["python", "main.py"]
