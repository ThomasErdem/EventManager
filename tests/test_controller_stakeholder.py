import unittest
from flask import Flask
from flask_testing import TestCase
from event_app import create_app, db
from event_app.bp_stakeholders.model_stakeholder import Stakeholder

class TestStakeholderViews(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app
    
    def setUp(self):
        db.create_all()
        
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        
    def test_do_stakeholder_add(self):
        # Simulate a POST request to add a new stakeholder
        response = self.client.post('/Stakeholders', data={
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone number': '123456789',
            'type': 'Customer',
            'company': 'ACME Corp'
        }, follow_redirects=True)
        
        self.assert200(response)
        self.assertIn(b'Stakeholder added!', response.data)
        
        # Check if the stakeholder is added to the database
        stakeholders = Stakeholder.query.all()
        self.assertEqual(len(stakeholders), 1)
        self.assertEqual(stakeholders[0].name, 'John Doe')
        # Add assertions for other attributes
        
    def test_do_stakeholder_add_invalid_name(self):
        # Simulate a POST request to add a new stakeholder with invalid name
        response = self.client.post('/Stakeholders', data={
            'name': '',
            'email': 'john@example.com',
            'phone number': '123456789',
            'type': 'Customer',
            'company': 'ACME Corp'
        }, follow_redirects=True)
        
        self.assert200(response)
        self.assertIn(b'Event name is too short!', response.data)
        
        # Check that no stakeholder is added to the database
        stakeholders = Stakeholder.query.all()
        self.assertEqual(len(stakeholders), 0)
        
    def test_do_stakeholder_update(self):
        # Create a stakeholder to update
        stakeholder = Stakeholder(name='Jane Smith', email='jane@example.com', phone_number='987654321', type='Supplier', company='XYZ Corp')
        db.session.add(stakeholder)
        db.session.commit()
        
        # Simulate a POST request to update the stakeholder
        response = self.client.post(f'/update-stakeholder/{stakeholder.id}', data={
            'name': 'Jane Johnson',
            'email': 'jane@example.com',
            'phone_number': '123456789',
            'type': 'Supplier',
            'company': 'XYZ Corp'
        }, follow_redirects=True)
        
        self.assert200(response)
        self.assertIn(b'Stakeholder updated successfully', response.data)
        
        # Check if the stakeholder is updated in the database
        updated_stakeholder = Stakeholder.query.get(stakeholder.id)
        self.assertEqual(updated_stakeholder.name, 'Jane Johnson')
        # Add assertions for other attributes
        
    def test_do_stakeholder_update_unauthorized(self):
        # Create a stakeholder owned by another user
        stakeholder = Stakeholder(name='Jane Smith', email='jane@example.com', phone_number='987654321', type='Supplier', company='XYZ Corp', user_id=2)
        db.session.add(stakeholder)
        db.session.commit()
        
        # Simulate a POST request to update the stakeholder
        response = self.client.post(f'/update-stakeholder/{stakeholder.id}', data={
            'name': 'Jane Johnson',
            'email': 'jane@example.com',
            'phone_number': '123456789',
            'type': 'Supplier',
            'company': 'XYZ Corp'
        }, follow_redirects=True)
        
        self.assert200(response)
        self.assertIn(b'You do not have permission to edit this stakeholder', response.data)
        
        # Check that the stakeholder is not updated in the database
        updated_stakeholder = Stakeholder.query.get(stakeholder.id)
        self.assertEqual(updated_stakeholder.name, 'Jane Smith')  # Name should remain the same
        
    def test_delete_stakeholder(self):
        # Create a stakeholder to delete
        stakeholder = Stakeholder(name='Jane Smith', email='jane@example.com', phone_number='987654321', type='Supplier', company='XYZ Corp')
        db.session.add(stakeholder)
        db.session.commit()
        
        # Simulate a POST request to delete the stakeholder
        response = self.client.post('/delete-stakeholder', json={
            'stakeholderId': stakeholder.id
        }, follow_redirects=True)
        
        self.assert200(response)
        
        # Check if the stakeholder is deleted from the database
        deleted_stakeholder = Stakeholder.query.get(stakeholder.id)
        self.assertIsNone(deleted_stakeholder)
        
    def test_delete_stakeholder_unauthorized(self):
        # Create a stakeholder owned by another user
        stakeholder = Stakeholder(name='Jane Smith', email='jane@example.com', phone_number='987654321', type='Supplier', company='XYZ Corp', user_id=2)
        db.session.add(stakeholder)
        db.session.commit()
        
        # Simulate a POST request to delete the stakeholder
        response = self.client.post('/delete-stakeholder', json={
            'stakeholderId': stakeholder.id
        }, follow_redirects=True)
        
        self.assert200(response)
        
        # Check that the stakeholder is not deleted from the database
        deleted_stakeholder = Stakeholder.query.get(stakeholder.id)
        self.assertIsNotNone(deleted_stakeholder)
        
if __name__ == '__main__':
    unittest.main()
