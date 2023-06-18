import unittest
from event_app import create_app, db
from event_app.bp_meetings.model_meeting import Meeting


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

    def test_do_meeting(self):
        response = self.app.get('/add-meeting')
        self.assertEqual(response.status_code, 302)

    def test_delete_meeting(self):
        response = self.app.get('/delete-meeting')
        self.assertEqual(response.status_code, 302)
    
    def test_update_meeting(self):
        response = self.app.get('/update-meeting')
        self.assertEqual(response.status_code, 302)

    def test_get_meeting(self):
        """Test retrieving a single meeting."""
        # Create a test meeting
        meeting = Meeting(
            subject='Test meeting',
            description='Test description',
            location='Test location',
            date='12-07-2023',
            time='12:30',
        )
        db.session.add(meeting)
        db.session.commit()

        # Simulate a GET request to retrieve the meeting by ID
        response = self.app.get(f'/meeting/{meeting.id}')

        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        self.assertEqual(response.json['subject'], 'Test meeting')  # Assert that the retrieved meeting matches the expected values

    def test_get_all_meetings(self):
        """Test retrieving all meetings."""
        # Create multiple test meetings
        meeting1 = Meeting(
            subject='Meeting 1',
            description='Description 1',
            location='Location 1',
            date='12-08-2023',
            time='12:35'
        )
        meeting2 = Meeting(
            subject='Meeting 2',
            description='Description 2',
            location='Location 2',
            date='12-09-2023',
            time='13:30'
        )
        db.session.add_all([meeting1, meeting2])
        db.session.commit()

        # Simulate a GET request to retrieve all meetings
        response = self.app.get('/meetings')

        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        meetings = response.json['meetings']
        self.assertEqual(len(meetings), 2)  # Assert that the number of retrieved meetings is correct

    def test_search_meetings(self):
        """Test searching for meetings."""
        # Create multiple test meetings
        meeting1 = Meeting(
            subject='Meeting 1',
            description='Description 1',
            location='Location 1',
            date='12-08-2023',
            time='12:35'
        )
        meeting2 = Meeting(
            subject='Meeting 2',
            description='Description 2',
            location='Location 2',
            date='12-09-2023',
            time='13:30'
        )
        db.session.add_all([meeting1, meeting2])
        db.session.commit()

        # Simulate a GET request to search for meetings by subject
        response = self.app.get('/meetings?search=Meeting 1')

        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        meetings = response.json['meetings']
        self.assertEqual(len(meetings), 1)  # Assert that only one meeting matches the search criteria

    def test_meeting_validation(self):
        """Test meeting data validation."""
        # Simulate a POST request with invalid data
        response = self.app.post('/add-meetings', data={
            'subject': 'A',  # Invalid name (too short)
            'description': 'Test description',
            'location': 'Test location',
            'date': 'Test date',
            'time': 'Test time'
        })
        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        self.assertIn(b'Meeting subject is too short!', response.data)  # Assert that the error message is displayed

        


if __name__ == '__main__':
    unittest.main()

