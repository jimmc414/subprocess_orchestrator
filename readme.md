# Subprocess Orchestrator

## Overview

The Subprocess Orchestrator is a flexible Python-based tool for managing and executing complex sequences of tasks. It's designed to be easily extendable, allowing you to define custom tasks, conditions, and workflows using a combination of YAML configuration and Python functions.

## Key Features

- Task definition using YAML configuration
- Support for subprocess execution, custom Python functions, and composite tasks
- Conditional task execution based on previous task results
- Integrated scheduling capabilities using APScheduler
- Extensible architecture for adding new task types and conditions

## Getting Started

1. Clone this repository
2. Install dependencies: `pip install pyyaml apscheduler`
3. Configure your tasks in `tasks_config.yaml`
4. Run the orchestrator: `python subprocess_orchestrator.py your_task_name`

## Extending the Orchestrator

### Adding New Task Types

1. Update `subprocess_orchestrator.py`:
   - Modify the `execute_task()` function to handle your new task type
   - Add any necessary helper functions

Example:
```python
def execute_task(task: Dict[str, Any], config: Dict[str, Any], context: Dict[str, Any]):
    # ... existing code ...
    elif task_type == 'your_new_task_type':
        result = your_new_task_function(task, context)
        context[f"{task_name}.result"] = result
    # ... existing code ...

def your_new_task_function(task: Dict[str, Any], context: Dict[str, Any]):
    # Implement your new task logic here
    pass
```

2. Update `tasks_config.yaml`:
   - Add your new task type to a task definition

Example:
```yaml
tasks:
  - name: example_new_task
    type: your_new_task_type
    # Add any necessary parameters for your new task type
```

### Adding New Utility Functions

1. Update `utils.py`:
   - Add your new function

Example:
```python
def your_new_utility_function(param1: str, param2: int) -> bool:
    # Implement your utility function
    pass
```

2. Update `tasks_config.yaml`:
   - Add your new function to the `functions` section

Example:
```yaml
functions:
  your_new_utility_function:
    path: "./utils.py"
    function: your_new_utility_function
```

### Creating Custom Conditions

1. Implement your condition function in `utils.py`
2. Use it in your task configuration:

```yaml
steps:
  - name: conditional_step
    type: subprocess
    command: ["your", "command"]
    run_if: your_custom_condition
```

### Extending Scheduling Capabilities

Modify the `schedule_tasks()` function in `subprocess_orchestrator.py` to support new scheduling patterns or integrate with different scheduling systems.

## Best Practices for Extension

1. **Maintain Modularity**: Keep new functionalities separate and focused.
2. **Update Documentation**: Document new task types, functions, or features in comments and this README.
3. **Error Handling**: Implement robust error handling for new features.
4. **Testing**: Create unit tests for new functions and integration tests for new task types.
5. **Configuration Driven**: Aim to make new features configurable via YAML when possible.
6. **Backward Compatibility**: Ensure extensions don't break existing functionality.

## Advanced Topics

### Custom Context Managers

For tasks requiring setup and teardown, consider implementing custom context managers:

```python
from contextlib import contextmanager

@contextmanager
def your_custom_context():
    # Setup
    try:
        yield
    finally:
        # Teardown
```

Use in `subprocess_orchestrator.py`:

```python
with your_custom_context():
    execute_task(task, config, context)
```

### Parallel Task Execution

For parallel execution of independent tasks, consider using Python's `concurrent.futures`:

```python
from concurrent.futures import ThreadPoolExecutor

def execute_parallel_tasks(tasks, config, context):
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(execute_task, task, config, context) for task in tasks]
        for future in futures:
            future.result()  # This will raise any exceptions that occurred
```

### Dynamic Task Generation

Implement a function to generate tasks dynamically based on runtime conditions:

```python
def generate_dynamic_tasks(context: Dict[str, Any]) -> List[Dict[str, Any]]:
    # Generate and return a list of tasks based on the current context
    pass
```

Use this in your main orchestration logic to add flexibility to your workflows.
