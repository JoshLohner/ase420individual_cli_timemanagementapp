import unittest
from datetime import datetime, timedelta
from main import Record


class TestRecord(unittest.TestCase):

    def test_convert_date(self):
        today_date = datetime.now().strftime('%Y/%m/%d')
        yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y/%m/%d')

        record_today = Record('today', '10:00', '12:00', 'Task 1', 'Tag 1')
        record_yesterday = Record('yesterday', '13:00', '15:00', 'Task 2', 'Tag 2')
        record_custom_date = Record('2023/01/01', '16:00', '18:00', 'Task 3', 'Tag 3')

        self.assertEqual(record_today.date, today_date)
        self.assertEqual(record_yesterday.date, yesterday_date)
        self.assertEqual(record_custom_date.date, '2023/01/01')

    def test_calculate_duration(self):
        record = Record('2023/01/01', '10:00', '12:30', 'Task 1', 'Tag 1')
        self.assertEqual(record.duration, '2:30:00')

    def test_validate_time_format(self):
        valid_time_str = '12:00'
        invalid_time_str = 'invalid_time'

        record_valid_time = Record('2023/01/01', valid_time_str, '13:00', 'Task 1', 'Tag 1')

        with self.assertRaises(ValueError):
            record_invalid_time = Record('2023/01/01', invalid_time_str, '13:00', 'Task 2', 'Tag 2')


if __name__ == '__main__':
    unittest.main()
