import unittest
from main import Database

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = Database(':memory:')

    def tearDown(self):
        self.db.close_connection()

    def test_create_table(self):
        self.assertTrue(self.table_exists('records'))

    def test_record_data(self):
        date = '2023/01/01'
        from_time = '10:00'
        to_time = '12:00'
        task = 'Test Task'
        tag = 'Test Tag'

        self.db.record_data(date, from_time, to_time, task, tag)

        result = self.db.query_all_records()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][0], '2:00:00')

    def test_query_all_records(self):
        self.db.record_data('2023/01/01', '10:00', '12:00', 'Task 1', 'Tag 1')
        self.db.record_data('2023/01/02', '13:00', '15:00', 'Task 2', 'Tag 2')

        result = self.db.query_all_records()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], '2:00:00')
        self.assertEqual(result[1][1], 'Task 2')


    def table_exists(self, table_name):
        query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        result = self.db.cursor.execute(query).fetchone()
        return result is not None

if __name__ == '__main__':
    unittest.main()
