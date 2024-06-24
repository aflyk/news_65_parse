import subprocess
import time
import platform
"""
описание почему platform а не sys
https://stackoverflow.com/questions/1854/how-to-identify-which-os-python-is-running-on
"""


if platform.system == 'Windows':
    python_executable = "./.venv/Scripts/python.exe"
else:
    python_executable = ".venv/bin/python"
second_script_path = "main.py"

while True:
    subprocess.call([python_executable, second_script_path])
    time.sleep(600)
