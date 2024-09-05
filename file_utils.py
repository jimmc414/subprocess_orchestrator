# file_utils.py

import os
from datetime import datetime, timedelta

def check_file_age(file_path: str, hours_threshold: int) -> bool:
    """
    Check if the file at file_path is older than hours_threshold.
    Returns True if the file is older than the threshold or if it doesn't exist.
    """
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist. Treating as exceeded threshold.")
        return True

    file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    age_threshold = datetime.now() - timedelta(hours=hours_threshold)

    if file_mod_time < age_threshold:
        print(f"File {file_path} is older than {hours_threshold} hours.")
        return True
    else:
        print(f"File {file_path} is not older than {hours_threshold} hours.")
        return False

def update_last_run(file_path: str) -> None:
    """
    Update the last run file with the current timestamp.
    """
    with open(file_path, 'w') as f:
        f.write(datetime.now().isoformat())
    print(f"Updated last run timestamp in {file_path}")

def file_updated(file_path: str, reference_time: str) -> bool:
    """
    Check if the file at file_path has been modified since reference_time.
    """
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return False

    file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    ref_time = datetime.fromisoformat(reference_time)

    if file_mod_time > ref_time:
        print(f"File {file_path} has been updated since {reference_time}.")
        return True
    else:
        print(f"File {file_path} has not been updated since {reference_time}.")
        return False