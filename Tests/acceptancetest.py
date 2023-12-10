import os
import subprocess
import time

def run_command(process, command):
    print(f"User: {command}")
    process.stdin.write(command + "\n")
    process.stdin.flush()
    time.sleep(1)

def run_acceptance_test():
    main_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "main.py"))
    process = subprocess.Popen(["python", main_path], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

    try:
        commands = [
            "record today 10:00 12:00 Task1 Tag1",
            "querydate today",
            "exit"
        ]

        for command in commands:
            run_command(process, command)

        output, _ = process.communicate()
        print("\nApplication Output:")
        print(output)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        process.terminate()

if __name__ == "__main__":
    run_acceptance_test()
