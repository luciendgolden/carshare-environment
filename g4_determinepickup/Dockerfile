FROM ubuntu:22.04

WORKDIR /code

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3 python3-pip swi-prolog

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8084

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 8084
COPY . .

CMD ["flask", "run"]
