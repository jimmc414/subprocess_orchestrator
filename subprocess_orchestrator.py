# subprocess_orchestrator.py

import os
import sys
import subprocess
import time
import logging
import yaml
import argparse
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from typing import List, Dict, Any
from importlib.util import spec_from_file_location, module_from_spec

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_config(config_path: str) -> Dict[str, Any]:
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def run_subprocess(command: List[str]) -> subprocess.CompletedProcess:
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info(f"Subprocess '{' '.join(command)}' completed successfully")
        return result
    except subprocess.CalledProcessError as e:
        logging.error(f"Subprocess '{' '.join(command)}' failed with error: {e}")
        raise

def load_function(path: str, function_name: str):
    spec = spec_from_file_location("module", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, function_name)

def wait_for_condition(condition: Dict[str, Any], max_wait_time: int, check_interval: int, context: Dict[str, Any]):
    start_time = time.time()
    while time.time() - start_time < max_wait_time:
        func_info = condition['type']
        args = condition['args']
        # Replace any template variables in args
        for key, value in args.items():
            if isinstance(value, str) and value.startswith('{{') and value.endswith('}}'):
                args[key] = context[value[2:-2]]
        
        if run_function(func_info, args):
            return True
        time.sleep(check_interval)
    return False

def run_function(func_info: Dict[str, str], args: Dict[str, Any] = None):
    func = load_function(func_info['path'], func_info['function'])
    try:
        result = func(**args) if args else func()
        logging.info(f"Function '{func_info['function']}' completed successfully")
        return result
    except Exception as e:
        logging.error(f"Error running function '{func_info['function']}': {str(e)}")
        raise

def execute_task(task: Dict[str, Any], config: Dict[str, Any], context: Dict[str, Any]):
    task_type = task['type']
    task_name = task['name']
    
    logging.info(f"Executing task: {task_name} (Type: {task_type})")
    
    try:
        if task_type == 'subprocess':
            result = run_subprocess(task['command'])
            context[f"{task_name}.result"] = result
        elif task_type == 'function':
            func_info = config['functions'][task['function']]
            result = run_function(func_info, task.get('args', {}))
            context[f"{task_name}.result"] = result
        elif task_type == 'wait':
            condition_met = wait_for_condition(task['condition'], task['max_wait_time'], task['check_interval'], context)
            if not condition_met:
                raise TimeoutError(f"Condition not met within {task['max_wait_time']} seconds")
        elif task_type == 'composite':
            execute_composite_task(task, config, context)
        else:
            raise ValueError(f"Unknown task type: {task_type}")
        
        logging.info(f"Task {task_name} completed successfully")
    except Exception as e:
        logging.error(f"Error in task {task_name}: {str(e)}")
        raise

def execute_composite_task(task: Dict[str, Any], config: Dict[str, Any], context: Dict[str, Any]):
    for step in task['steps']:
        if 'run_if' in step:
            condition = step['run_if']
            if isinstance(condition, str):
                if not context.get(condition, False):
                    logging.info(f"Skipping step '{step['name']}' as condition '{condition}' is not met")
                    continue
            elif callable(condition):
                if not condition(context):
                    logging.info(f"Skipping step '{step['name']}' as custom condition is not met")
                    continue
        execute_task(step, config, context)

def subprocess_orchestrator(config: Dict[str, Any], task_name: str):
    tasks = config['tasks']
    task = next((t for t in tasks if t['name'] == task_name), None)
    
    if not task:
        logging.error(f"Task '{task_name}' not found in configuration")
        sys.exit(1)
    
    context = {}
    try:
        execute_task(task, config, context)
        logging.info(f"Task '{task_name}' completed successfully")
    except Exception as e:
        logging.error(f"Error in task '{task_name}': {str(e)}")
        sys.exit(1)

def schedule_tasks(config: Dict[str, Any]):
    scheduler = BackgroundScheduler()
    for task in config['tasks']:
        if 'schedule' in task:
            scheduler.add_job(
                subprocess_orchestrator,
                trigger=task['schedule']['type'],
                **task['schedule']['args'],
                args=[config, task['name']]
            )
    return scheduler

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subprocess Orchestrator")
    parser.add_argument("task", nargs='?', help="Name of the task to run")
    parser.add_argument("--config", default="tasks_config.yaml", help="Path to the YAML configuration file")
    parser.add_argument("--schedule", action="store_true", help="Run as a scheduler")
    args = parser.parse_args()

    config = load_config(args.config)
    
    if args.schedule:
        scheduler = schedule_tasks(config)
        scheduler.start()
        try:
            while True:
                time.sleep(1)
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
    elif args.task:
        subprocess_orchestrator(config, args.task)
    else:
        parser.print_help()
        sys.exit(1)