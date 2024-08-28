# Subprocess Orchestrator

The Subprocess Orchestrator is a tool designed to manage and execute complex sequences of custom tasks and conditions. It supports running subprocesses, custom Python functions, and composite tasks defined in a YAML configuration file.

## Features

- Task definition using YAML configuration
- Support for subprocess execution, custom Python functions, and composite tasks
- Conditional task execution based on previous task results
- Task-specific instance checking to prevent multiple runs of the same task
- External function loading for custom task logic

## Requirements

- Python 3.6+
- PyYAML
- psutil

## Installation

1. Clone this repository or download the `subprocess_orchestrator.py` file.
2. Install the required dependencies:

   ```
   pip install PyYAML psutil
   ```

3. Create your YAML configuration file (default name: `tasks_config.yaml`).

## Configuration

Tasks are defined in a YAML file. Here's an example structure:

```yaml
tasks:
  - name: task_name
    type: subprocess|function|composite
    command: ["command", "arg1", "arg2"]  # for subprocess
    function: function_name  # for function
    steps:  # for composite
      - name: step1
        type: subprocess|function
        # ... step details ...

functions:
  function_name:
    path: "/path/to/python/file.py"
    function: function_name
```

### Task Types

1. **subprocess**: Executes a command-line process
2. **function**: Runs a custom Python function
3. **composite**: Executes a series of steps, which can be subprocesses or functions

## Usage

Run the orchestrator from the command line, specifying the task to execute:

```
python subprocess_orchestrator.py task_name
```

You can specify a custom configuration file using the `--config` option:

```
python subprocess_orchestrator.py task_name --config custom_config.yaml
```

## Example: Stratus Task

The "stratus" task demonstrates a composite task that:

1. Checks the age of a specific file
2. Runs a command if the file is older than a threshold
3. Copies an output file
4. Runs a Python script to process data

To run the stratus task:

```
python subprocess_orchestrator.py stratus
```

## Extending the Orchestrator

To add new task types or functionality:

1. Update the `execute_task()` function in `subprocess_orchestrator.py`
2. Add corresponding logic in the YAML configuration
3. Implement any necessary custom functions in separate Python files

