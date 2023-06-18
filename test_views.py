import unittest
from main import app

class BPViewsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_calendar(self):
        response = self.app.get('/calendar')
        self.assertEqual(response.status_code, 302)

    def test_events(self):
        response = self.app.get('/event-list')
        self.assertEqual(response.status_code, 302)

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)

    def test_meeting(self):
        response = self.app.get('/meeting-list')
        self.assertEqual(response.status_code, 302)

    def test_stakeholder(self):
        response = self.app.get('/stakeholder-list')
        self.assertEqual(response.status_code, 302)

    def test_task(self):
        response = self.app.get('/task-list')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
