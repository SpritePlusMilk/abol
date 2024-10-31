FROM python:3.12
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends supervisor

COPY requirements.txt requirements.txt
COPY supervisor/supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisor/serv.conf /etc/supervisor/conf.d/app.conf

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD python manage.py migrate && python manage.py collectstatic --noinput
CMD /usr/bin/supervisord -c /etc/supervisor/supervisord.conf --nodaemon