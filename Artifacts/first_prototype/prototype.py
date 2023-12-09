import sqlite3
from datetime import datetime

# Function to initialize the SQLite database
def initialize_database(database_path):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            from_time TEXT,
            to_time TEXT,
            task TEXT,
            tag TEXT
        )
    ''')

    connection.commit()
    connection.close()

# Function to record data into the SQLite database
def record_data(database_path):
    date = input("Enter date (YYYY-MM-DD): ")
    from_time = input("Enter start time (HH:MM): ")
    to_time = input("Enter end time (HH:MM): ")
    task = input("Enter task description: ")
    tag = input("Enter tag: ")

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Insert data into the 'tasks' table
    cursor.execute('''
        INSERT INTO tasks (date, from_time, to_time, task, tag)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, from_time, to_time, task, tag))

    connection.commit()
    connection.close()
    print("Recorded successfully.")

# Function to query data from the SQLite database based on tag, date, or task
def query_data(database_path):
    print("\nQuery Options:")
    print("1. Query by Tag")
    print("2. Query by Date")
    print("3. Query by Task")
    print("4. Back to main menu")

    choice = input("Enter your choice (1/2/3/4): ")

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    if choice == '1':
        tag = input("Enter tag to query: ")
        cursor.execute('''
            SELECT * FROM tasks
            WHERE tag = ?
        ''', (tag,))
    elif choice == '2':
        date = input("Enter date to query (YYYY-MM-DD): ")
        cursor.execute('''
            SELECT * FROM tasks
            WHERE date = ?
        ''', (date,))
    elif choice == '3':
        task = input("Enter task to query: ")
        cursor.execute('''
            SELECT * FROM tasks
            WHERE task LIKE ?
        ''', ('%' + task + '%',))
    elif choice == '4':
        connection.close()
        return
    else:
        print("Invalid choice. Please enter 1, 2, 3, or 4.")
        connection.close()
        return

    # Fetch and print the results
    results = cursor.fetchall()
    for row in results:
        print(row)

    connection.close()

# Main function
def main():
    database_path = '../../tasks.db'

    # Initialize the database
    initialize_database(database_path)

    while True:
        print("\nOptions:")
        print("1. Record task")
        print("2. Query tasks")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            record_data(database_path)
        elif choice == '2':
            query_data(database_path)
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == '__main__':
    main()
