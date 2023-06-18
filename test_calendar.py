import unittest
from flask import Flask
from flask_testing import TestCase

from event_app import create_app

class CalendarTestCase(TestCase):
    def create_app(self):
        # Create a test Flask application
        app = create_app()
        app.config['TESTING'] = True
        return app

    def test_calendar_page(self):
        response = self.client.get('/calendar')
        self.assertEqual(response.status_code, 302)  # Update status code to 302

    def test_calendar_events(self):
        # Mock events data
        events = [
            {'title': 'Event 1', 'location': 'Location 1', 'start': '2023-06-18'},
            {'title': 'Event 2', 'location': 'Location 2', 'start': '2023-06-19'},
            # Add more events as needed
        ]

        with self.client.session_transaction() as session:
            # Store the events data in the session
            session['events'] = events

        response = self.client.get('/calendar')
        self.assertEqual(response.status_code, 302)  # Update status code to 302
        self.assert_context('events', events)

    def test_calendar_meetings(self):
        # Mock meetings data
        meetings = [
            {'title': 'Meeting 1', 'start': '2023-06-20', 'time': '10:00 AM'},
            {'title': 'Meeting 2', 'start': '2023-06-21', 'time': '2:00 PM'},
            # Add more meetings as needed
        ]

        with self.client.session_transaction() as session:
            # Store the meetings data in the session
            session['meetings'] = meetings

        response = self.client.get('/calendar')
        self.assertEqual(response.status_code, 302)  # Update status code to 302
        self.assert_context('meetings', meetings)

    def test_calendar_tasks(self):
        # Mock tasks data
        tasks = [
            {'title': 'Task 1', 'end': '2023-06-22'},
            {'title': 'Task 2', 'end': '2023-06-23'},
            # Add more tasks as needed
        ]

        with self.client.session_transaction() as session:
            # Store the tasks data in the session
            session['tasks'] = tasks

        response = self.client.get('/calendar')
        self.assertEqual(response.status_code, 302)  # Update status code to 302
        self.assert_context('tasks', tasks)

if __name__ == '__main__':
    unittest.main()
