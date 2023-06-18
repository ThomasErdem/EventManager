import unittest
from event_app import create_app, db
from event_app.bp_tasks.model_task import Task
from event_app.bp_tasks.utils import generateRandomColors


class TaskTestCase(unittest.TestCase):
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


    def test_do_task(self):
        """Test the do_task route."""
        # Simulate a POST request with valid data
        response = self.app.post('/add-task', data={
            'data': 'Test data',
            'note': 'Test note',
            'priority': 'Urgent',
            'status': 'On hold',
            'date': '23-07-2024',
            'deadline': '25-07-2024',
        })
        self.assertEqual(response.status_code, 200)  # Assert that the response is successful

        # Assert that the task was added to the database
        task = Task.query.filter_by(data='Test data').first()
        self.assertIsNotNone(task)  # Assert that the task exists
        self.assertEqual(task.status, 'On hold')  # Assert other attributes of the task

        # Simulate a POST request with invalid data
        response = self.app.post('/add-task', data={
            'data': '',
            'note': 'Test note',
            'priority': 'Urgent',
            'status': 'On hold',
            'date': 'Test date',
            'deadline': '25-07-2024',
        })
        self.assertEqual(response.status_code, 200)  # Assert that the response is successful
        self.assertIn(b'Task name is too short!', response.data)  # Assert that the error message is displayed

    def test_delete_task(self):
        """Test the delete-task route."""
        # Create a test task
        task = Task(data='Test data', note='Test note', priority='Urgent', status='On hold', date='23-04-2024', deadline='25-07-2024')
        db.session.add(task)
        db.session.commit()

        # Simulate a POST request to delete the task
        response = self.app.post('/delete-task', json={'taskId': task.id})

        self.assertEqual(response.status_code, 200)  # Assert that the response is successfulself

        # Assert that the task was deleted from the database
        deleted_task = Task.query.get(task.id)
        self.assertIsNone(deleted_task)  # Assert that the task no longer exists

    def test_update_task(self):
        """Test the update-task route."""
        # Create a test task
        task = Task(data='Test data', note='Test note', priority='Urgent', status='On hold', date='23-04-2024', deadline='25-07-2024')
        db.session.add(task)
        db.session.commit()

        # Simulate a POST request to update the task
        response = self.app.post(f'/update-task/{task.id}', data={
            'data': 'Updated data',
            'note': 'Updated note',
            'priority': 'Updated priority',
            'status': 'Updated status',
            'date': 'Updated date',
            'deadline': 'Updated deadline',
        })

        self.assertEqual(response.status_code, 302)  # Assert that the response is a redirect

        # Retrieve the updated task from the database
        updated_task = Task.query.get(task.id)

        self.assertEqual(updated_task.data, 'Updated data')  # Assert that the name was updated
        self.assertEqual(updated_task.note, 'updated note')  # Assert that the note was updated
        self.assertEqual(updated_task.priority, 'Updated priority')  # Assert that the priority level was updated
        self.assertEqual(updated_task.status, 'Updated status')  # Assert that the status was updated
        self.assertEqual(updated_task.date, 'Updated date')  # Assert that the date was updated
        self.assertEqual(updated_task.deadline, 'Updated deadline')  # Assert that the deadline was updated

        # Simulate a POST request to update a non-existing task
        response = self.app.post('/update-task/1000', data={
            'data': 'Updated data',
            'note': 'Updated note',
            'priority': 'Updated priority',
            'status': 'Updated status',
            'date': 'Updated date',
            'deadline': 'Updated deadline',
        })

        self.assertEqual(response.status_code, 302)  # Assert that the response is a redirect


class RandomColorsTestCase(unittest.TestCase):
    def test_generate_random_colors(self):
        # Test generating 5 random colors
        colors = generateRandomColors(5)
        self.assertEqual(len(colors), 5)  # Check if the correct number of colors is generated
        
        # Test generating 0 random colors
        colors = generateRandomColors(0)
        self.assertEqual(len(colors), 0)  # Check if an empty list is returned

        # Test generating a large number of random colors
        colors = generateRandomColors(10000)
        self.assertEqual(len(colors), 10000)  # Check if the correct number of colors is generated

        # Test generating negative number of random colors
        colors = generateRandomColors(-5)
        self.assertEqual(len(colors), 0)  # Check if an empty list is returned


if __name__ == '__main__':
    unittest.main()
