#!/bin/bash
set -e

export FLASK_APP=manage:app
flask create_table
# flask test
# flask run --host=0.0.0.0
gunicorn --workers 4 \
    -b 0.0.0.0:5000 \
    --log-config gunicorn.conf \
    --worker-class gevent wsgi:app
