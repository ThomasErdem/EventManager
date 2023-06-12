import unittest
from flask import Flask
from flask_testing import TestCase
from event_app import create_app, db
from event_app.bp_events.model_event import Event
from event_app.bp_events.controller_event import get_events

class EventTestCase(TestCase):
    def create_app(self):
        # Create a Flask app instance for testing
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        # Set up any necessary dependencies or configurations for the tests
        db.create_all()

    def tearDown(self):
        # Clean up after the tests
        db.session.remove()
        db.drop_all()

    def test_do_event(self):
        # Test the 'do_event' route
        response = self.client.post('/add-events')
        self.assert200(response)
        # Add more assertions based on the expected behavior of the route

    def test_get_events(self):
        # Test the 'get_events' function
        # Mock some events in the database
        event1 = Event(name='Event 1', description='Description 1', location='Location 1')
        event2 = Event(name='Event 2', description='Description 2', location='Location 2')
        db.session.add_all([event1, event2])
        db.session.commit()

        # Call the 'get_events' function
        events = get_events()

        # Assert the returned events
        self.assertEqual(len(events), 2)
        self.assertEqual(events[0]['title'], 'Event 1')
        self.assertEqual(events[1]['title'], 'Event 2')
        # Add more assertions based on the expected behavior of the function

    def test_delete_event(self):
        # Test the 'delete_event' route
        # Mock an event in the database
        event = Event(name='Event 1', description='Description 1', location='Location 1')
        db.session.add(event)
        db.session.commit()

        # Call the 'delete_event' route
        response = self.client.post('/delete-event', json={'eventId': event.id})

        # Assert the response
        self.assert200(response)
        # Add more assertions based on the expected behavior of the route

    def test_update_event(self):
        # Test the 'update_event' route
        # Mock an event in the database
        event = Event(name='Event 1', description='Description 1', location='Location 1')
        db.session.add(event)
        db.session.commit()

        # Call the 'update_event' route
        response = self.client.post(f'/update-event/{event.id}')

        # Assert the response
        self.assert200(response)
        # Add more assertions based on the expected behavior of the route

if __name__ == '__main__':
    unittest.main()
