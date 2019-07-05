FROM python:3.7-alpine

COPY requirements-docker.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8000", "app:app"]
