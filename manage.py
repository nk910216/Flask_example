# -*- coing: utf-8
import pytest

from server import init_app
from server.extensions import db

# Init the app and connect to the manager
app = init_app()

@app.cli.command()
def test():
    """ Runs the tests
    """
    return pytest.main(['-s', 'server/tests', ])


@app.cli.command()
def create_table():
    """ Creates the table
    """
    db.create_all()
    db.session.commit()
