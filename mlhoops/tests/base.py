from flask_testing import TestCase
from flask.config import Config

from mlhoops.driver import app
from mlhoops.db.init_db import drop_db, init_db, init_db_data


class TestBase(TestCase):
    """
    Base class for all test classes
    """
    def __init__(self, *args, **kwargs):
        super(TestBase, self).__init__(*args, **kwargs)
        self.config = Config(root_path='../..')
        app.error_handler_spec[None] = {}
        app.config.update({'PRESERVE_CONTEXT_ON_EXCEPTION': False})

    def create_app(self):
        with app.app_context():
            drop_db()
            init_db()
            init_db_data()
            app.config.update({'TESTING': True})
        return app
