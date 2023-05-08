FROM python:3.9.7-slim-buster

ARG LOCAL_PATH

WORKDIR /app

COPY ${LOCAL_PATH} /app

RUN pip install -r requirements.txt

CMD ["adev", "runserver", "--port", "8080","--livereload"]