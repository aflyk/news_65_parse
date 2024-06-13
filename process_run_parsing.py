import subprocess
import time

python_executable = ".venv/bin/python"
second_script_path = "main.py"

while True:
    subprocess.call([python_executable, second_script_path])
    time.sleep(600)
