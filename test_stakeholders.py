import unittest
from event_app import create_app, db
from event_app.bp_stakeholders.model_stakeholder import Stakeholder


class MeetingTestCase(unittest.TestCase):
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

    def test_do_stakeholder(self):
        response = self.app.get('/add-stakeholder')
        self.assertEqual(response.status_code, 302)

    def test_delete_stakeholder(self):
        response = self.app.get('/delete-stakeholder')
        self.assertEqual(response.status_code, 302)
    
    def test_update_stakeholder(self):
        response = self.app.get('/update-stakeholder')
        self.assertEqual(response.status_code, 302)

    def test_get_stakeholder(self):
        """Test retrieving a single stakeholder."""
        # Create a test stakeholder
        stakeholder = Stakeholder(
            name='Test name',
            email='Test email',
            phone_number='Test phone number',
            type='Test type',
            company='Test company',
        )
        db.session.add(stakeholder)
        db.session.commit()

        # Simulate a GET request to retrieve the event by ID
        response = self.app.get(f'/stakeholder/{stakeholder.id}')

        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        self.assertEqual(response.json['name'], 'Test name')  # Assert that the retrieved event matches the expected values

    def test_get_all_stakeholders(self):
        """Test retrieving all stakeholders."""
        # Create multiple test stakeholders
        stakeholder1 = Stakeholder(
            name='Test name 1',
            email='Test email 1',
            phone_number='Test phone number 1',
            type='Test type 1',
            company='Test company 1',
        )
        stakeholder2 = Stakeholder(
            name='Test name 2',
            email='Test email 2',
            phone_number='Test phone number 2',
            type='Test type 2',
            company='Test company 2',
        )
        db.session.add_all([stakeholder1, stakeholder2])
        db.session.commit()

        # Simulate a GET request to retrieve all stakeholders
        response = self.app.get('/stakeholders')

        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        Stakeholders = response.json['stakeholders']
        self.assertEqual(len(Stakeholders), 2)  # Assert that the number of retrieved stakeholders is correct

    def test_search_stakeholders(self):
        """Test searching for stakeholders."""
        # Create multiple test stakeholders
        stakeholder1 = Stakeholder(
            name='Test name 1',
            email='Test email 1',
            phone_number='Test phone number 1',
            type='Test type 1',
            company='Test company 1',
        )
        stakeholder2 = Stakeholder(
            name='Test name 2',
            email='Test email 2',
            phone_number='Test phone number 2',
            type='Test type 2',
            company='Test company 2',
        )
        db.session.add_all([stakeholder1, stakeholder2])
        db.session.commit()

        # Simulate a GET request to search for stakeholders by subject
        response = self.app.get('/stakeholders?search=Stakeholder 1')

        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        stakeholders = response.json['stakeholders']
        self.assertEqual(len(stakeholders), 1)  # Assert that only one event matches the search criteria

    def test_stakeholder_validation(self):
        """Test stakeholder data validation."""
        # Simulate a POST request with invalid data
        response = self.app.post('/add-stakeholders', data={
            'name': 'A',  # Invalid name (too short)
            'email': 'Test email',
            'phone_number': 'Test phone number',
            'type': 'Test type',
            'company': 'Test company'
        })
        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        self.assertIn(b'Stakeholder name is too short!', response.data)  # Assert that the error message is displayed

        


if __name__ == '__main__':
    unittest.main()

