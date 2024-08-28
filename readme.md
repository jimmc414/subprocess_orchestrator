# Subprocess Orchestrator

The Subprocess Orchestrator is a tool designed to manage and execute sequences of tasks. It supports running subprocesses, custom Python functions, and composite tasks defined in a YAML configuration file.

## Features

- Task definition using YAML configuration
- Support for subprocess execution, custom Python functions, and composite tasks
- Conditional task execution based on previous task results
- Task-specific instance checking to prevent multiple runs of the same task
- External function loading for custom task logic
- Waiting periods with configurable conditions

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
        type: subprocess|function|wait
        # ... step details ...

functions:
  function_name:
    path: "/path/to/python/file.py"
    function: function_name
```

## Usage

Run the orchestrator from the command line, specifying the task to execute:

```
python subprocess_orchestrator.py task_name
```

You can specify a custom configuration file using the `--config` option:

```
python subprocess_orchestrator.py task_name --config custom_config.yaml
```

## Example Use Case: Stratus Task

The "stratus" task demonstrates a composite task that processes data based on file age. Here's how it works:

1. **Check File Age**: 
   - Checks if the file `m:\spbw\output.csv` is older than 24 hours.
   - If true, sets `file_age_exceeded` to `True` in the context.

2. **Run Acuthin**:
   - If `file_age_exceeded` is `True`, runs the command:
     `\\mp-cp\bin\acuthin mp-cp f1 stratus`
   - This command presumably generates or updates the `output.csv` file.

3. **Wait for Acuthin**:
   - Waits up to 10 minutes, checking every 30 seconds if `m:\spbw\output.csv` has been updated since the acuthin command started.

4. **Copy Output**:
   - If the file was updated, copies it to a new location:
     `copy m:\spbw\output.csv \\thinclient\d$\cp\edi\spbw /y`

5. **Run Python Script**:
   - Executes a Python script for further processing:
     `python T:\EDISHARE\PYTHON\AOD_Report\process_data.py`

To run this task:

```
python subprocess_orchestrator.py stratus
```

This example demonstrates:
- Conditional execution based on file age
- Running external processes
- Waiting for file updates with a timeout
- Copying files
- Running additional scripts

After the main task, you can update the last run time:

```
python subprocess_orchestrator.py update_last_run
```

This updates the timestamp on `m:\spbw\output.csv`, preparing for the next run.

## Extending the Orchestrator

To add new task types or functionality:

1. Update the `execute_task()` function in `subprocess_orchestrator.py`
2. Add corresponding logic in the YAML configuration
3. Implement any necessary custom functions in separate Python files

## Troubleshooting

- Ensure all paths in the YAML configuration are correct and accessible
- Check that custom functions are properly implemented and return expected results
- Verify that required permissions are set for running subprocesses and accessing files