FROM python:3.6

RUN mkdir -p /var/log/gunicorn

WORKDIR /usr/src/app

ADD . /usr/src/app
RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
