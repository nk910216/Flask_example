from unittest import TestCase

from server.extensions import db
from flask import current_app


class BaseTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = cls.create_app()

    @classmethod
    def create_app(cls):

        app = current_app

        db.create_all()
        db.session.commit()

        return app.test_client()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
