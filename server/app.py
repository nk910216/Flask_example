from flask import Flask

def init_app():
    """ Init the whole application
    """

    app = Flask(__name__)

    return app