import unittest
import sqlite3
from main import Database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database(':memory:')  # Use an in-memory database for testing

    def tearDown(self):
        self.db.close_connection()

    def test_create_table(self):
        # Test if the table is created successfully
        self.assertTrue(self.table_exists('records'))

    def test_record_data(self):
        # Test if recording data works as expected
        date = '2023/01/01'
        from_time = '10:00'
        to_time = '12:00'
        task = 'Test Task'
        tag = 'Test Tag'

        self.db.record_data(date, from_time, to_time, task, tag)

        # Check if the recorded data exists in the database
        result = self.db.query_all_records()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], '2:00:00')  # Assuming a 2-hour duration for this test

    def test_query_all_records(self):
        # Test if querying all records works as expected
        self.db.record_data('2023/01/01', '10:00', '12:00', 'Task 1', 'Tag 1')
        self.db.record_data('2023/01/02', '13:00', '15:00', 'Task 2', 'Tag 2')

        result = self.db.query_all_records()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], '2:00:00')
        self.assertEqual(result[1][1], 'Task 2')

    # Add more tests for other methods as needed

    def table_exists(self, table_name):
        # Helper method to check if a table exists in the database
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        result = self.db.cursor.execute(query).fetchone()
        return result is not None

if __name__ == '__main__':
    unittest.main()
