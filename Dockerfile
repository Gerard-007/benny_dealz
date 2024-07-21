FROM python:3.11.4-slim-bullseye

COPY ./requirements.txt /app/requirements.txt

RUN set -ex \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app

ADD . .

#EXPOSE 8000
#
#CMD [ "gunicorn", "--bind", ":8000", "--workers", "3", "benny_dealz.wsgi:application"]

CMD gunicorn benny_dealz.wsgi:application --bind 0.0.0.0:$PORT