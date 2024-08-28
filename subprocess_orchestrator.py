tasks:
  - name: stratus
    type: composite
    steps:
      - name: check_file_age
        type: function
        function: check_file_age
        args:
          file_path: "T:\\EDISHARE\\PYTHON\\AOD_Report\\last_run.txt"
          hours_threshold: 24
      - name: run_acuthin
        type: subprocess
        command: ["\\\\mp-cp\\bin\\acuthin", "mp-cp", "f1", "stratus"]
        run_if: file_age_exceeded
      - name: copy_output
        type: subprocess
        command: ["copy", "m:\\spbw\\output.csv", "\\\\thinclient\\d$\\cp\\edi\\spbw", "/y"]
      - name: run_python_script
        type: subprocess
        command: ["python", "T:\\EDISHARE\\PYTHON\\AOD_Report\\process_data.py"]

  - name: other_task
    type: subprocess
    command: ["echo", "This is another task"]

functions:
  check_file_age:
    path: "T:\\EDISHARE\\PYTHON\\AOD_Report\\file_utils.py"
    function: check_file_age