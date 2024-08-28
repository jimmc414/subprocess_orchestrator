import os
import sys
import subprocess
import time
import psutil
import logging
import yaml
import argparse
from typing import List, Dict, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_path: str) -> Dict[str, Any]:
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def is_task_running(task_name: str) -> bool:
    current_process = psutil.Process()
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['name'] == current_process.name() and \
           len(process.info['cmdline']) > 2 and \
           process.info['cmdline'][1] == task_name and \
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

def run_function(func_name: str):
    try:
        # This assumes the function is defined in the global namespace
        globals()[func_name]()
    except KeyError:
        logging.error(f"Function '{func_name}' not found")
        raise
    except Exception as e:
        logging.error(f"Error running function '{func_name}': {str(e)}")
        raise

def execute_task(task: Dict[str, Any]):
    logging.info(f"Executing task: {task['name']}")
    if task['type'] == 'subprocess':
        run_subprocess(task['command'])
    elif task['type'] == 'function':
        run_function(task['function'])
    else:
        logging.error(f"Unknown task type: {task['type']}")
        raise ValueError(f"Unknown task type: {task['type']}")

def subprocess_orchestrator(config: Dict[str, Any], task_name: str):
    tasks = config['tasks']
    task = next((t for t in tasks if t['name'] == task_name), None)
    
    if not task:
        logging.error(f"Task '{task_name}' not found in configuration")
        sys.exit(1)
    
    # Execute prerequisites
    for prereq in task.get('prerequisites', []):
        subprocess_orchestrator(config, prereq)
    
    # Execute the task
    try:
        execute_task(task)
        logging.info(f"Task '{task_name}' completed successfully")
    except Exception as e:
        logging.error(f"Error in task '{task_name}': {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subprocess Orchestrator")
    parser.add_argument("task", help="Name of the task to run")
    parser.add_argument("--config", default="tasks_config.yaml", help="Path to the YAML configuration file")
    args = parser.parse_args()

    if is_task_running(args.task):
        logging.info(f"An instance of task '{args.task}' is already running. Exiting.")
        sys.exit(0)
    
    config = load_config(args.config)
    subprocess_orchestrator(config, args.task)