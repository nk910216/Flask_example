# -*- coing: utf-8
import unittest

from server import init_app

# Init the app and connect to the manager
app = init_app()

@app.cli.command()
def test():
    """ Runs the tests
    """
    tests = unittest.TestLoader().discover('server', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1
