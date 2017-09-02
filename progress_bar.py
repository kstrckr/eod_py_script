import subprocess
import os
import shlex

def clear_screen():
    """clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_progress_bar(final_length):
    ping_call = ['ping', '91.198.174.192', '-t']
    python_call = ['python', 'fake_input.py']

    proc = subprocess.Popen(python_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    while proc.poll() is None:
        line = proc.stdout.readline().decode()
        if line:
            print("\033[37m{}\033[0m".format(line.strip()))

print_progress_bar(10)
