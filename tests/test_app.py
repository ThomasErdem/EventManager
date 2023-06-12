import unittest
from flask import current_app
from flask_testing import TestCase
from event_app.bp_stakeholders.model_stakeholder import Stakeholder
from event_app import create_app, db


class FlaskAppTests(TestCase):

    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory SQLite database for testing
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_app_exists(self):
        self.assertIsNotNone(current_app)

    def test_index_route(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assert_template_used('general/home.html')

    def test_invalid_route(self):
        response = self.client.get('/invalid')
        self.assert404(response)

    def test_database_connection(self):
        response = self.client.get('/')
        self.assert200(response)
        self.assertIsNotNone(db.session.connection())

    def test_empty_database(self):
        response = self.client.get('/')
        self.assert200(response)
        stakeholders = db.session.query(Stakeholder).all()
        self.assertEqual(len(stakeholders), 0)

if __name__ == '__main__':
    unittest.main()
