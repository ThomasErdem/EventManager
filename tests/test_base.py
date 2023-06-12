from event_app import create_app
import unittest


class FlaskTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app
        self.client = self.app.test_client()

    def test_index(self):
        response = self.client.get("/")
        status_code = response.status_code
        self.assertEqual(status_code, 200)


if __name__ == "__main__":
    unittest.main()
