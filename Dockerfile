FROM python:3.9.7-slim-buster

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["adev", "runserver", "--port", "8080","--livereload"]