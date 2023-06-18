import unittest
from event_app import create_app, db
from event_app.bp_events.model_event import Event


class EventTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment."""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/test_event_management'

        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the test environment."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_do_event(self):
        response = self.app.get('/add-event')
        self.assertEqual(response.status_code, 302)

    def test_delete_event(self):
        response = self.app.get('/delete-event')
        self.assertEqual(response.status_code, 302)
    
    def test_update_event(self):
        response = self.app.get('/update-event')
        self.assertEqual(response.status_code, 302)

    def test_get_event(self):
        """Test retrieving a single event."""
        # Create a test event
        event = Event(
            name='Test event',
            description='Test description',
            location='Test location',
            date='12-07-2023',
            budget='10000',
            program='Test program',
            category='Test category'
        )
        db.session.add(event)
        db.session.commit()

        # Simulate a GET request to retrieve the event by ID
        response = self.app.get(f'/event/{event.id}')

        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        self.assertEqual(response.json['name'], 'Test event')  # Assert that the retrieved event matches the expected values

    def test_get_all_events(self):
        """Test retrieving all events."""
        # Create multiple test events
        event1 = Event(
            name='Event 1',
            description='Description 1',
            location='Location 1',
            date='12-07-2023',
            budget='10000',
            program='Program 1',
            category='Category 1'
        )
        event2 = Event(
            name='Event 2',
            description='Description 2',
            location='Location 2',
            date='13-07-2023',
            budget='20000',
            program='Program 2',
            category='Category 2'
        )
        db.session.add_all([event1, event2])
        db.session.commit()

        # Simulate a GET request to retrieve all events
        response = self.app.get('/events')

        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        events = response.json['events']
        self.assertEqual(len(events), 2)  # Assert that the number of retrieved events is correct

    def test_search_events(self):
        """Test searching for events."""
        # Create multiple test events
        event1 = Event(
            name='Event 1',
            description='Description 1',
            location='Location 1',
            date='12-07-2023',
            budget='10000',
            program='Program 1',
            category='Category 1'
        )
        event2 = Event(
            name='Event 2',
            description='Description 2',
            location='Location 2',
            date='13-07-2023',
            budget='20000',
            program='Program 2',
            category='Category 2'
        )
        db.session.add_all([event1, event2])
        db.session.commit()

        # Simulate a GET request to search for events by name
        response = self.app.get('/events?search=Event 1')

        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        events = response.json['events']
        self.assertEqual(len(events), 1)  # Assert that only one event matches the search criteria

    def test_event_validation(self):
        """Test event data validation."""
        # Simulate a POST request with invalid data
        response = self.app.post('/add-events', data={
            'name': 'A',  # Invalid name (too short)
            'description': 'Test description',
            'location': 'Test location',
            'date': 'Test date',
            'budget': 'Test budget',
            'program': 'Test program',
            'category': 'Test category'
        })
        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        self.assertIn(b'Event name is too short!', response.data)  # Assert that the error message is displayed

        # ...


if __name__ == '__main__':
    unittest.main()
