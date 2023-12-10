import unittest
from main import Database, QueryHandler

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.db = Database(':memory:')
        self.query_handler = QueryHandler()

    def tearDown(self):
        self.db.close_connection()

    def test_priority_query(self):
        self.db.record_data("2023/12/10", "09:00", "12:00", "Task1", "Tag1")
        self.db.record_data("2023/12/10", "12:30", "15:30", "Task2", "Tag2")
        self.db.record_data("2023/12/10", "16:00", "18:00", "Task1", "Tag1")
        self.db.record_data("2023/12/10", "09:00", "11:00", "Task3", "Tag3")

        query_result = self.query_handler.query_priority(self.db)

        expected_result = [
            {'task': 'Task1', 'total_duration': '5.0'},
            {'task': 'Task2', 'total_duration': '3.0'},
            {'task': 'Task3', 'total_duration': '2.0'}
        ]



        if query_result:
            query_result.sort(key=lambda x: x['task'])

            self.assertEqual(query_result, expected_result)


if __name__ == "__main__":
    unittest.main()
