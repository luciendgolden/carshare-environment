FROM python:3.9

RUN apt-get update && apt-get install -y libffi-dev libssl-dev bzip2

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8089

ENV FLASK_APP=app/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8089

CMD ["flask", "run"]