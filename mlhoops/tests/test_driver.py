from mlhoops.tests.base import TestBase


class TestDriver(TestBase):
    """
    Test class for mlhoops/driver.py
    """
    def test_driver(self):
        res = self.client.get("/")
        self.assertEqual(res.get_data(as_text=True), "Hello World!")
