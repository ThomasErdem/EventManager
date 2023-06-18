import unittest
from flask import Flask, session
from werkzeug.security import check_password_hash
from flask_testing import TestCase
from event_app import create_app, db
from event_app.bp_user.model_user import User

class AuthTests(TestCase):
    def create_app(self):
        # Create a test Flask application
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/test_event_management'
        return app

    def setUp(self):
        # Create the database tables and a test user
        db.create_all()
        user = User(email='test@example.com', first_name='Test', password='password')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        # Remove the database tables after each test
        db.session.remove()
        db.drop_all()

    def test_login_success(self):
        # Test successful login
        response = self.client.post('/login', data={'email': 'test@example.com', 'password': 'password'})
        self.assertRedirects(response, '/bp_home/do_home')
        with self.client.session_transaction() as sess:
            self.assertEqual(sess['user_id'], 1)  # Assuming the test user has ID 1

    def test_login_incorrect_password(self):
    # Check if the email exists in the table
        user = User.query.filter_by(email='test@example.com').first()
        if user:
            # Update the existing entry
            user.password = 'new_password'
            db.session.commit()
        else:
            # Insert a new entry
            response = self.app.post('/login', data={
                'email': 'test@example.com',
                'password': 'password'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Incorrect password', response.data)


    def test_login_nonexistent_email(self):
        # Test login with nonexistent email
        response = self.client.post('/login', data={'email': 'nonexistent@example.com', 'password': 'password'})
        self.assert200(response)
        self.assertIn(b'Email does not exist', response.data)

    def test_logout(self):
        # Test logout
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1  # Assuming the test user is logged in
        response = self.client.get('/logout')
        self.assertRedirects(response, '/login')
        with self.client.session_transaction() as sess:
            self.assertNotIn('user_id', sess)

    def test_sign_up_success(self):
        # Test successful sign up
        response = self.client.post('/sign-up', data={'email': 'newuser@example.com', 'firstName': 'New', 'password1': 'password', 'password2': 'password'})
        self.assertRedirects(response, '/bp_home/do_home')
        with self.client.session_transaction() as sess:
            self.assertEqual(sess['user_id'], 2)  # Assuming the new user has ID 2

    def test_sign_up_existing_email(self):
        # Test sign up with existing email
        response = self.client.post('/sign-up', data={'email': 'test@example.com', 'firstName': 'New', 'password1': 'password', 'password2': 'password'})
        self.assert200(response)
        self.assertIn(b'Email already exists', response.data)

    

if __name__ == '__main__':
    unittest.main()
