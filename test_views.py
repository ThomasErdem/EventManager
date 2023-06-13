import unittest
from  main import app
'''
python -m unittest test_filename.py

coverage run -m unittest discover

coverage report


'''



class bp_views(unittest.TestCase):

    def test_calendar(self):
        tester = app.test_client(self)
        response = tester.get('/calendar')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<h1>Welcome {{current_user.first_name}}, this is your personal agenda</h1>", response.data)

    def test_events(self):
        tester = app.test_client(self)
        response = tester.get('/event-list')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<h1>EVENTS</h1>", response.data)

    def test_home(self):
        tester = app.test_client(self)
        response = tester.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<h2>Welcome, {{ current_user.first_name }}!</h2> ", response.data)

    def test_meeting(self):
        tester = app.test_client(self)
        response = tester.get('/meeting-list')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<h1>MEETINGS</h1> ", response.data)

    def test_stakeholder(self):
        tester = app.test_client(self)
        response = tester.get('/stakeholder-list')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"<h1>STAKEHOLDERS</h1>", response.data)


    def test_task(self):
        tester = app.test_client(self)
        response = tester.get('/task-list')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"<h1>TO DO LIST</h1>", response.data)




