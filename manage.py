# -*- coing: utf-8
import pytest
import pymysql
from sqlalchemy import create_engine

from server import init_app
from server.extensions import db

# for mysql
pymysql.install_as_MySQLdb()

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
    engine = db.get_engine()
    db_connect_url = engine.url

    # get all info for the connection
    db_name = engine.name
    db_host = db_connect_url.host
    db_port = db_connect_url.port
    db_database = db_connect_url.database
    db_username = db_connect_url.username
    db_password = db_connect_url.password

    db_port = ':' + str(db_port) if db_port else ''
    # connect to database using another engine
    connect_url = '{0}://{1}:{2}@{3}{4}'.format(db_name, db_username,
                                                db_password, db_host,
                                                db_port)
    db_engine = create_engine(connect_url)
    existing_dbs = db_engine.execute("SHOW DATABASES")
    existing_dbs = [d[0] for d in existing_dbs]

    # create database if not exist
    if db_database not in existing_dbs:
        db_engine.execute("CREATE DATABASE IF NOT EXISTS {}".
                          format(db_database))
        print('create database')

    # create tables
    db.create_all()
    db.session.commit()
