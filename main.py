import sqlite3
from datetime import datetime, timedelta


class Database:
    def __init__(self, db_name='my_database.db'):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY,
                date TEXT,
                from_time TEXT,
                to_time TEXT,
                duration TEXT,  -- Added a new column for duration
                task TEXT,
                tag TEXT
            )
        ''')
        self.connection.commit()

    def record_data(self, date, from_time, to_time, task, tag):
        duration = self.calculate_duration(from_time, to_time)
        self.cursor.execute('''
            INSERT INTO records (date, from_time, to_time, duration, task, tag)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (date, from_time, to_time, duration, task, tag))
        self.connection.commit()

    def calculate_duration(self, from_time, to_time):
        from_datetime = datetime.strptime(from_time, '%H:%M')
        to_datetime = datetime.strptime(to_time, '%H:%M')
        duration = to_datetime - from_datetime
        return str(duration)

    def query_data(self, query_object):
        return query_object.execute(self)

    def query_all_records(self):
        self.cursor.execute('''
            SELECT duration, task FROM records
        ''')
        return self.cursor.fetchall()

    def close_connection(self):
        self.connection.close()


class Record:
    def __init__(self, date, from_time, to_time, task, tag):
        self.date = self.convert_date(date)
        self.from_time = self.validate_time_format(from_time)
        self.to_time = self.validate_time_format(to_time)
        self.duration = self.calculate_duration(from_time, to_time)
        self.task = task.lower()
        self.tag = tag.lower()

    def convert_date(self, date):
        if date.lower() == 'today':
            return datetime.now().strftime('%Y/%m/%d')
        elif date.lower() == 'yesterday':
            yesterday = datetime.now() - timedelta(days=1)
            return yesterday.strftime('%Y/%m/%d')
        else:
            return date

    def calculate_duration(self, from_time, to_time):
        from_datetime = datetime.strptime(from_time, '%H:%M')
        to_datetime = datetime.strptime(to_time, '%H:%M')
        duration = to_datetime - from_datetime
        return str(duration)

    def validate_time_format(self, time_str):
        try:
            datetime.strptime(time_str, '%H:%M')
            return time_str
        except ValueError:
            raise ValueError("Invalid time format. Use HH:MM")


# Add a new class for priority query
class QueryPriority:
    def execute(self, database):
        database.cursor.execute('''
            SELECT task, SUM(duration) as total_duration
            FROM records
            GROUP BY task
            ORDER BY total_duration DESC
        ''')
        return database.cursor.fetchall()


class QueryTask:
    def __init__(self, task):
        self.task = task

    def execute(self, database):
        database.cursor.execute('''
            SELECT * FROM records WHERE task = ?
        ''', (self.task,))
        return database.cursor.fetchall()


class QueryTag:
    def __init__(self, tag):
        self.tag = tag

    def execute(self, database):
        database.cursor.execute('''
            SELECT * FROM records WHERE tag = ?
        ''', (self.tag,))
        return database.cursor.fetchall()


class QueryDate:
    def __init__(self, date):
        self.date = self.convert_date(date)

    def convert_date(self, date):
        if date.lower() == 'today':
            return datetime.now().strftime('%Y/%m/%d')
        elif date.lower() == 'yesterday':
            yesterday = datetime.now() - timedelta(days=1)
            return yesterday.strftime('%Y/%m/%d')
        else:
            return date

    def execute(self, database):
        database.cursor.execute('''
            SELECT * FROM records WHERE date = ?
        ''', (self.date,))
        return database.cursor.fetchall()


class QueryDateRange:
    def __init__(self, start_date, end_date):
        self.start_date = self.convert_date(start_date)
        self.end_date = self.convert_date(end_date)

    def convert_date(self, date):
        if date.lower() == 'today':
            return datetime.now().strftime('%Y/%m/%d')
        elif date.lower() == 'yesterday':
            yesterday = datetime.now() - timedelta(days=1)
            return yesterday.strftime('%Y/%m/%d')
        else:
            return date

    def execute(self, database):
        database.cursor.execute('''
            SELECT * FROM records WHERE date BETWEEN ? AND ?
        ''', (self.start_date, self.end_date))
        return database.cursor.fetchall()


class CommandLoop:
    def __init__(self, main_app):
        self.main_app = main_app

    def start(self):
        while True:
            command = input("Enter command: ")
            if command.lower() == 'exit':
                self.main_app.close()
                break
            else:
                self.main_app.process_command(command)


class QueryHandler:

    def query_priority(self, database):
        query_object = QueryPriority()
        result = query_object.execute(database)

        if result:
            print("Combined Duration for Tasks:")
            for record in result:
                print("Task: {}, Combined Duration: {}".format(record[0], record[1]))
        else:
            print("No records found.")

    def query_task(self, task, database):
        query_object = QueryTask(task)
        result = query_object.execute(database)

        if result:
            print("Matching records for task {}: ".format(task))
            for record in result:
                print(record)
        else:
            print("No records found for the given task.")

    def query_tag(self, tag, database):
        query_object = QueryTag(tag)
        result = query_object.execute(database)

        if result:
            print("Matching records for tag {}: ".format(tag))
            for record in result:
                print(record)
        else:
            print("No records found for the given tag.")

    def query_date(self, date, database):
        query_object = QueryDate(date)
        result = query_object.execute(database)

        if result:
            print("Matching records for date {}: ".format(date))
            for record in result:
                print(record)
        else:
            print("No records found for the given date.")

    def query_date_range(self, start_date, end_date, database):
        query_object = QueryDateRange(start_date, end_date)
        result = query_object.execute(database)

        if result:
            print("Matching records for date range {} to {}: ".format(start_date, end_date))
            for record in result:
                print(record)
        else:
            print("No records found for the given date range.")


class MainApp:
    def __init__(self):
        self.db = Database()
        self.query_handler = QueryHandler()

    def process_command(self, command):
        parts = command.split()
        operation = parts[0].lower()

        if operation == 'record':
            self.record(parts[1:])
        elif operation == 'querytask':
            self.query_handler.query_task(parts[1], self.db)
        elif operation == 'querytag':
            self.query_handler.query_tag(parts[1], self.db)
        elif operation == 'querydate':
            self.query_handler.query_date(parts[1], self.db)
        elif operation == 'report':
            self.query_handler.query_date_range(parts[1], parts[2], self.db)
        elif operation == 'priority':
            self.query_handler.query_priority(self.db)
        else:
            print("Invalid command. Supported commands: record, querytask, querytag, querydate, report, priority, exit")

    def record(self, data):
        if len(data) != 5:
            print("Invalid record command. Use: record DATE FROMTIME TOTIME TASK TAG")
            return

        record_object = Record(*data)
        self.db.record_data(record_object.date, record_object.from_time, record_object.to_time, record_object.task,
                            record_object.tag)
        print("Record added successfully.")

    def close(self):
        self.db.close_connection()


if __name__ == "__main__":
    main_app = MainApp()
    command_loop = CommandLoop(main_app)
    command_loop.start()
