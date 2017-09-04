import subprocess
import os
import math

def clear_screen():
    """clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

class Spinner:
    def __init__(self):
        self.spinner_state = [
            '-',
            '\\',
            '|',
            '/',
        ]
        self.spinner_now = 0

    def update_spinner(self):
        self.spinner_now += 1
        if self.spinner_now == len(self.spinner_state):
            self.spinner_now = 0

        output = self.spinner_state[self.spinner_now]
        return output


def print_progress_bar(final_length):

    python_call = ['python', 'fake_input.py']
    spinner = Spinner()
    current_progress = 0
    

    proc = subprocess.Popen(python_call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    while proc.poll() is None:
        line = proc.stdout.readline().decode()
        if line:
            current_progress += 1
            percent_complete = int((current_progress/final_length) * 100)
            progress_bar_now = math.floor(0.1 * percent_complete)
            progress_bar_viz = '|' * int(progress_bar_now) + '_' * (9-int(progress_bar_now))
            spinner_viz = spinner.update_spinner()
            final_output = '[{}]\n{}/{} {}%\n{}'.format(spinner_viz,current_progress, final_length, percent_complete, progress_bar_viz)
            clear_screen()
            print(final_output)
            #print("\033[37m{}\033[0m".format(line.strip()))


print_progress_bar(60)
