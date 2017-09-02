import subprocess
import os
import shlex

def clear_screen():
    """clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_progress_bar(final_length):

    proc = subprocess.Popen(['ping', '91.198.174.192', '-t'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    while proc.poll() is None:
        line = proc.stdout.readline().decode()
        if line:
            print("\033[37m{}\033[0m".format(line.strip()[-6:]))

print_progress_bar(10)
