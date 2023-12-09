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
                task TEXT,
                tag TEXT
            )
        ''')
        self.connection.commit()

    def record_data(self, date, from_time, to_time, task, tag):
        self.cursor.execute('''
            INSERT INTO records (date, from_time, to_time, task, tag)
            VALUES (?, ?, ?, ?, ?)
        ''', (date, from_time, to_time, task, tag))
        self.connection.commit()

    def query_data(self, query_object):
        return query_object.execute(self)

    def close_connection(self):
        self.connection.close()

class Record:
    def __init__(self, date, from_time, to_time, task, tag):
        self.date = self.convert_date(date)
        self.from_time = from_time
        self.to_time = to_time
        self.task = task
        self.tag = tag

    def convert_date(self, date):
        if date.lower() == 'today':
            return datetime.now().strftime('%Y/%m/%d')
        elif date.lower() == 'yesterday':
            yesterday = datetime.now() - timedelta(days=1)
            return yesterday.strftime('%Y/%m/%d')
        else:
            return date

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

class Main:
    def __init__(self):
        self.db = Database()

    def process_command(self, command):
        parts = command.split()
        operation = parts[0].lower()

        if operation == 'record':
            self.record(parts[1:])
        elif operation == 'querytask':
            self.query_task(parts[1])
        elif operation == 'querytag':
            self.query_tag(parts[1])
        elif operation == 'querydate':
            self.query_date(parts[1])
        else:
            print("Invalid command. Supported commands: record, querytask, querytag, querydate")

    def record(self, data):
        if len(data) != 5:
            print("Invalid record command. Use: record DATE FROMTIME TOTIME TASK TAG")
            return

        record_object = Record(*data)
        self.db.record_data(record_object.date, record_object.from_time, record_object.to_time, record_object.task, record_object.tag)
        print("Record added successfully.")

    def query_task(self, task):
        query_object = QueryTask(task)
        result = query_object.execute(self.db)

        if result:
            print("Matching records for task {}: ".format(task))
            for record in result:
                print(record)
        else:
            print("No records found for the given task.")

    def query_tag(self, tag):
        query_object = QueryTag(tag)
        result = query_object.execute(self.db)

        if result:
            print("Matching records for tag {}: ".format(tag))
            for record in result:
                print(record)
        else:
            print("No records found for the given tag.")

    def query_date(self, date):
        query_object = QueryDate(date)
        result = query_object.execute(self.db)

        if result:
            print("Matching records for date {}: ".format(date))
            for record in result:
                print(record)
        else:
            print("No records found for the given date.")

    def close(self):
        self.db.close_connection()

if __name__ == "__main__":
    main_app = Main()
    command_loop = CommandLoop(main_app)
    command_loop.start()
