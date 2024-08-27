import os
import sys
import subprocess
import time
import psutil
import logging
from typing import Callable, List, Dict

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def is_already_running() -> bool:
    current_process = psutil.Process()
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['name'] == current_process.name() and \
           process.info['cmdline'] == current_process.cmdline() and \
           process.info['pid'] != current_process.pid:
            return True
    return False

def run_subprocess(command: List[str]) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info(f"Subprocess '{' '.join(command)}' completed successfully")
        return result
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess '{' '.join(command)}' failed with error: {e}")
        raise

def custom_function_1():
    logging.info("Running custom function 1")
    # Add your custom logic here
    time.sleep(2)  # Simulating some work

def custom_function_2():
    logging.info("Running custom function 2")
    # Add your custom logic here
    time.sleep(3)  # Simulating some work

def subprocess_orchestrator():
    tasks = [
        {
            "name": "Task 1",
            "type": "subprocess",
            "command": ["echo", "Hello, World!"],
            "prerequisites": [],
        },
        {
            "name": "Task 2",
            "type": "function",
            "function": custom_function_1,
            "prerequisites": ["Task 1"],
        },
        {
            "name": "Task 3",
            "type": "subprocess",
            "command": ["ls", "-l"],
            "prerequisites": ["Task 1"],
        },
        {
            "name": "Task 4",
            "type": "function",
            "function": custom_function_2,
            "prerequisites": ["Task 2", "Task 3"],
        },
    ]

    completed_tasks = set()

    while len(completed_tasks) < len(tasks):
        for task in tasks:
            if task["name"] not in completed_tasks and all(prereq in completed_tasks for prereq in task["prerequisites"]):
                try:
                    logging.info(f"Starting {task['name']}")
                    if task["type"] == "subprocess":
                        run_subprocess(task["command"])
                    elif task["type"] == "function":
                        task["function"]()
                    completed_tasks.add(task["name"])
                    logging.info(f"Completed {task['name']}")
                except Exception as e:
                    logging.error(f"Error in {task['name']}: {str(e)}")
                    sys.exit(1)

    logging.info("All tasks completed successfully")

if __name__ == "__main__":
    if is_already_running():
        logging.info("An instance of this script is already running. Exiting.")
        sys.exit(0)
    
    subprocess_orchestrator()