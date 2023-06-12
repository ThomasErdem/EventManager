import unittest
from flask import Flask
from flask_testing import TestCase
from datetime import datetime
from main import create_app
from event_app import db
from event_app.bp_events import Event
from event_app.bp_meetings import Meeting 
from event_app.bp_tasks import Task


class FlaskAppTests(TestCase):
    def create_app(self):
        # Create a test app
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        # Set up the test database
        db.create_all()
        # Add sample data for testing
        # ...

    def tearDown(self):
        # Clean up the test database
        db.session.remove()
        db.drop_all()

    def test_do_home(self):
        # Test case for the do_home route
        with self.client:
            response = self.client.get('/')
            self.assert200(response)
            self.assert_template_used('general/home.html')
            # Add more assertions to check the content of the response

if __name__ == '__main__':
    unittest.main()
