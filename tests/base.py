from flask_testing import TestCase
from flask import Flask

from mlhoops.driver import app
from mlhoops.db.init_db import drop_db, init_db, init_db_data


class TestBase(TestCase):
    """
    Base class for all test classes
    """

    def __init__(self):
        super(TestBase, self).__init__()
        app.error_handler_spec[None] = {}
        app.config.update({'PRESERVE_CONTEXT_ON_EXCEPTION': False})

    def create_app(self):
        app = Flask(__name__)
        app.config.update({'TESTING': True})
        return app

    def setUp(self):
        with app.app_context():
            drop_db()
            init_db()
            init_db_data()
