import unittest
from flask import Flask, render_template
from flask_login import current_user
from flask_testing import TestCase
from event_app import create_app, db
from event_app.bp_user.model_user import User
from event_app.bp_events.model_event import Event
from event_app.bp_events.views_event import bp_events


class EventListTestCase(TestCase):
    def create_app(self):
        # Create a Flask app instance for testing
        app = create_app()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.register_blueprint(bp_events)
        return app

    def setUp(self):
        # Set up any necessary dependencies or configurations for the tests
        db.create_all()

    def tearDown(self):
        # Clean up after the tests
        db.session.remove()
        db.drop_all()

    def test_do_event_list(self):
        # Test the 'do_event_list' route

        # Create some dummy events
        event1 = Event(name='Event 1', description='Description 1', location='Location 1')
        event2 = Event(name='Event 2', description='Description 2', location='Location 2')
        db.session.add_all([event1, event2])
        db.session.commit()

        # Log in a user (optional, depending on your authentication setup)
        # Set the current_user to a dummy user
        dummy_user = User(id=1, username='testuser', email='test@example.com')
        with self.client.session_transaction() as session:
            session['user_id'] = dummy_user.id

        # Call the 'do_event_list' route
        response = self.client.get('/event-list')

        # Assert the response
        self.assert200(response)
        self.assertTemplateUsed('event/event_list.html')

        # Verify that the events are passed to the template
        rendered_template = response.data.decode('utf-8')
        self.assertIn(event1.name, rendered_template)
        self.assertIn(event2.name, rendered_template)

        # Verify that the current_user is passed to the template
        self.assertEqual(current_user, dummy_user)


if __name__ == '__main__':
    unittest.main()
