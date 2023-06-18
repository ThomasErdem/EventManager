import unittest
from  main import create_app, db
from event_app.bp_events.controller_event import do_event, get_events
from event_app.bp_events.model_event import Event 
from event_app.bp_meetings.model_meeting import Meeting
'''
python -m coverage run -m unittest

python -m coverage report

coverage report


'''



    
class EventTestCase(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        app = create_app()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/event_management'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """Tear down the test environment."""
        db.session.remove()
        db.drop_all()

    def test_do_event(self):
    #Test the do_event function.
    # Simulate a POST request with valid data
        response = self.app.post('/add-events', data={
            'name': 'Test Event',
            'description': 'Test description',
            'location': 'Test location',
            'budget': '1000',
            'program': 'Test program',
            'category': 'Test category'
        })
        self.assertEqual(response.status_code, 200)  # Assert that the response is successful

        # Assert that the event was added to the database
        event = Event.query.filter_by(name='Test Event').first()
        self.assertIsNotNone(event)  # Assert that the event exists
        self.assertEqual(event.description, 'Test description')  # Assert other attributes of the event

        # Simulate a POST request with invalid data
        response = self.app.post('/add-events', data={
            'name': '',
            'description': 'Test description',
            'location': 'Test location',
            'budget': '1000',
            'program': 'Test program',
            'category': 'Test category'
        })
        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        self.assertIn(b'Event name is too short!', response.data)  # Assert that the error message is displayed

    def test_get_events(self):
        """Test the get_events function."""
        # Create a test event
        event = Event(name='Test Event', description='Test description', location='Test location', budget='1000')
        db.session.add(event)
        db.session.commit()

        # Call the get_events function
        with self.app:
            response = self.app.get('/get-events')

        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        self.assertIn(b'Test Event', response.data)  # Assert that the test event is displayed in the response



    def test_do_meeting(self):
    #Test the do_meeting function.
    # Simulate a POST request with valid data
        response = self.app.post('/add-meetings', data={
            'subject': 'Test meeting',
            'description': 'Test description',
            'location': 'Test location',
            'date': '25-06-2023',
            'time': '12:30',
        })
        self.assertEqual(response.status_code, 200)  # Assert that the response is successful

        # Assert that the event was added to the database
        meeting = Meeting.query.filter_by(name='Test meeting').first()
        self.assertIsNotNone(meeting)  # Assert that the event exists
        self.assertEqual(meeting.description, 'Test description')  # Assert other attributes of the event

        # Simulate a POST request with invalid data
        response = self.app.post('/add-meetings', data={
            'subject': '',
            'description': 'Test description',
            'location': 'Test location',
            'date': 'Test',
            'time': 'Test',
        })
        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        self.assertIn(b'Meeting subject is too short!', response.data)  # Assert that the error message is displayed

    def test_get_meetings(self):
        """Test the get_meetings function."""
        # Create a test event
        meeting = Meeting(subject='Test Meeting', description='Test description', location='Test location', date='25-06-2023', time='12:30')
        db.session.add(meeting)
        db.session.commit()

        # Call the get_events function
        with self.app:
            response = self.app.get('/get-meetings')

        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        self.assertIn(b'Test meeting', response.data)  # Assert that the test meeting is displayed in the response

if __name__ == '__main__':
    unittest.main()