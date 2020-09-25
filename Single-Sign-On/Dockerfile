FROM python:3.8.5-slim-buster
ENV PYTHONUNBUFFERRED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY ./src/ /code/
CMD python manage.py migrate \
        && python manage.py viga_setup \
        && gunicorn sso_server.wsgi --workers=3 --bind 0.0.0.0:8000
