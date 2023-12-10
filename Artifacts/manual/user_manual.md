# CLI Time Management Application

## Introduction
This is a time management application. It allows you to record and query 
tasks based on date, time, and tags through simple commands.

## Starting the program
Navigate into the folder where main.py is located. Open a terminal, and run
python main.py. This will open the program up, where it will prompt you to
enter a command.

## Different Commands

### Record
The record commands allows the user to enter their data/information into
the database. The specific format to use the command is:

**record date fromtime totime task tag**

Some caveats-

-Date must be entered in the formats: yyyy/mm/dd | tomorrow | 
yesterday

-Fromtime and totime must follow the XX:XX format. 
### Report
The report command displays all activities recorded within a time range,
specified by the user. The specific format for this command is:

**report date date**

### Priority
The priority command displays all of the activities that you have done by
the task name. It displays them in a list from highest duration to lowest.
The specific format for this command is:

**priority**

### Exit
The exit command closes out of the program. The specific format for
this command is:

**exit**

### Query Variants
The query commands allow the user to retrieve the information that 
they have stored in their database. QueryDate allows the user to see
all database entries that have the specified date. The specific format for
it is:

**querydate date**

The querytask command allows users to see all database entries that have
the same task. The specific format for it is:

**querytask task**

The querytag command allows users to see all database entries that have
the same tag. The specific format for it is:

**querytask tag**

