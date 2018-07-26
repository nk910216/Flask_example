#!/bin/bash
set -e

export FLASK_APP=manage:app
flask run --host=0.0.0.0