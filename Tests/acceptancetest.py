import os
import subprocess
import time

def run_command(process, command):
    print(f"User: {command}")
    process.stdin.write(command + "\n")
    process.stdin.flush()
    time.sleep(1)  # Allow some time for the application to respond

def run_acceptance_test():
    # Get the absolute path to main.py
    main_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "main.py"))

    # Start the application in a separate process
    process = subprocess.Popen(["python", main_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    try:
        # Simulate user interaction
        commands = [
            "record today 10:00 12:00 Task1 Tag1",
            "querydate today",
            "exit"
        ]

        for command in commands:
            run_command(process, command)

        # Capture and print the application's output
        output, _ = process.communicate()
        print("\nApplication Output:")
        print(output)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the process
        process.terminate()

if __name__ == "__main__":
    run_acceptance_test()
