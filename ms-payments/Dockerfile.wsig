FROM python:3.10-slim-bullseye

ENV FLASK_CONTEXT=development
ENV PYTHONUNBUFFERED=1
ENV PATH=$PATH:/home/flask/.local/bin

RUN groupadd flaskgroup && useradd -m -g flaskgroup -s /bin/bash flask
RUN chown -R flask:flaskgroup /home/flask
RUN apt-get update
RUN apt-get install -y build-essential curl iputils-ping
RUN apt-get install -y python3-dev build-essential libpq-dev python3-psycopg2
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false
RUN rm -rf /var/lib/apt/lists/*
RUN echo "flask ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN mkdir -p /home/flask/app/e-commerce/
ADD . /home/flask/app/e-commerce/

WORKDIR /home/flask/app/e-commerce

USER flask
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["uwsgi", "--wsgi-file","app.py", "uwsgi.ini"]
