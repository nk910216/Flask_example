#!/bin/bash
set -e

export FLASK_APP=manage:app
flask create_table
# flask test
flask run --host=0.0.0.0