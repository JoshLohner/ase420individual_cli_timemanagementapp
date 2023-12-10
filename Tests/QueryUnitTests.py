import unittest
from main import Database, QueryPriority, QueryTask, QueryTag, QueryDate, QueryDateRange

class TestQueryPriority(unittest.TestCase):

    def setUp(self):
        self.db = Database(':memory:')
        self.query_priority = QueryPriority()

    def tearDown(self):
        self.db.close_connection()

    def test_execute(self):
        # Test if priority query execution works as expected
        self.db.record_data('2023/01/01', '10:00', '12:00', 'Task 1', 'Tag 1')
        self.db.record_data('2023/01/01', '13:00', '15:00', 'Task 2', 'Tag 2')

        result = self.query_priority.execute(self.db)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], 'Task 2')


class TestQueryTask(unittest.TestCase):

    def setUp(self):
        self.db = Database(':memory:')
        self.query_task = QueryTask('Task 1')

    def tearDown(self):
        self.db.close_connection()

    def test_execute(self):
        # Test if task query execution works as expected
        self.db.record_data('2023/01/01', '10:00', '12:00', 'Task 1', 'Tag 1')
        self.db.record_data('2023/01/01', '13:00', '15:00', 'Task 2', 'Tag 2')

        result = self.query_task.execute(self.db)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][4], '2:00:00')

class TestQueryTag(unittest.TestCase):

    def setUp(self):
        self.db = Database(':memory:')
        self.query_tag = QueryTag('Tag 1')

    def tearDown(self):
        self.db.close_connection()

    def test_execute(self):
        # Test if tag query execution works as expected
        self.db.record_data('2023/01/01', '10:00', '12:00', 'Task 1', 'Tag 1')
        self.db.record_data('2023/01/01', '13:00', '15:00', 'Task 2', 'Tag 2')

        result = self.query_tag.execute(self.db)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][5], 'Task 1')

class TestQueryDate(unittest.TestCase):

    def setUp(self):
        self.db = Database(':memory:')
        self.query_date = QueryDate('2023/01/01')

    def tearDown(self):
        self.db.close_connection()

    def test_execute(self):
        # Test if date query execution works as expected
        self.db.record_data('2023/01/01', '10:00', '12:00', 'Task 1', 'Tag 1')
        self.db.record_data('2023/01/01', '13:00', '15:00', 'Task 2', 'Tag 2')

        result = self.query_date.execute(self.db)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][1], '2023/01/01')
        self.assertEqual(result[1][3], '15:00')

class TestQueryDateRange(unittest.TestCase):

    def setUp(self):
        self.db = Database(':memory:')
        self.query_date_range = QueryDateRange('2023/01/01', '2023/01/02')

    def tearDown(self):
        self.db.close_connection()

    def test_execute(self):
        # Test if date range query execution works as expected
        self.db.record_data('2023/01/01', '10:00', '12:00', 'Task 1', 'Tag 1')
        self.db.record_data('2023/01/02', '13:00', '15:00', 'Task 2', 'Tag 2')

        result = self.query_date_range.execute(self.db)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][2], '10:00')
        self.assertEqual(result[1][4], '2:00:00')

if __name__ == '__main__':
    unittest.main()
