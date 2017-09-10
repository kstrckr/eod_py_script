#! /usr/bin/python

#Kurt Strecker
#kstrecker@gilt.com
# v0.8 - 09/08/2017

import csv
import os
import sys
import subprocess
import argparse
import re
import math


class VmLogin:
    def __init__(self, user_name, password, environment):
        self.user_name = user_name
        self.password = password
        self.environment = environment

    def authenticate(self):
        subprocess.call([
            'zm',
            '-s',
            self.environment,
            '--username',
            self.user_name,
            '--password',
            self.password,
            'getcredentials'])

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

def clear_screen():
    """clears the screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def parse_the_args():
    """checks for the option PATH argument and returns the path if present"""
    parser = argparse.ArgumentParser(
        description="pre-check the selects folder for completeness before ingestion"
        )
    parser.add_argument('-p', '--path', help="pass the url from root to your SELECTS folder")
    args = parser.parse_args()
    return args.path

def parse_paths(path_arg=None):
    """if path_arg is passed from the eod.py execution it's used, if no arguments provided
    it will prompt the user to drag the SELECTS folder into the terminal window
    """

    if path_arg:
        selects_folder_path = path_arg.strip()
    else:
        print('type QUIT to exit or,')
        selects_folder_path = raw_input('drag SELECTS folder into window and press ENTER: >>  ')
        if selects_folder.lower() == 'quit':
            exit()
        elif not selects_folder_path:
            clear_screen()
            print("must drag SELECTS folder into window or type QUIT to exit\n\n")
            parse_paths()
        selects_folder_path = selects_folder_path.strip()

    metadata_csv_path = '/{}/photoshoot_{}_metadata.csv'.format(
        selects_folder_path, selects_folder_path[-13:-8])

    selects_folder_string = re.search(
        r'\d{2}_\d{2}_\d{4}_KY_STUDIO_\d{2}\w?_\d+_SELECTS',
        selects_folder_path)

    return (selects_folder_path, metadata_csv_path, selects_folder_string)

def open_csv(csv_path):
    """loads the photoshoot app's csv file, returns only a list of SKU filenames"""
    try:
        with open(csv_path, 'rb') as csv_data:
            reader = csv.reader(csv_data)
            photoshoot_app_skus = list(reader)
            del photoshoot_app_skus[0]
            skus_from_photo_app = [sku[0] for sku in photoshoot_app_skus]
            return skus_from_photo_app
    except IOError:
        print('No CSV found at \033[31m{}\033[0m, or path to SELECTS is wrong\n'
              'Make sure the CSV is in the correct location and the path is correct:'.format(csv_path))
        user_prompt = raw_input('Press ENTER to try again or enter QUIT to exit: >>  ')
        if user_prompt.lower() == 'quit':
            print("\033[32mEOD process ended\033[0m")
            exit()
        else:
            return open_csv(csv_path)

def load_file_names(selects_path):
    """returns a list of processed filenames from the SELECTS folder"""
    path = selects_path
    dirs = os.listdir(path)
    file_names = [file for file in dirs]
    return file_names

def update_csv(csv_path, selects_folder_path, selects_folder_string):

    new_rows = []
    print(selects_folder_path)
    selects_folder = re.search(
        r'\d{2}_\d{2}_\d{4}_KY_STUDIO_\d{2}\w?_\d+_SELECTS',
        selects_folder_path)
    #print(selects_folder.group(0))

    with open(csv_path, 'r') as csv_data:
        reader = csv.reader(csv_data)
        header = reader.next()
        new_rows.append(header)

        for row in reader:
            new_row = row
            new_sku = "{}/{}".format(selects_folder_string, row[0])
            new_row[0] = new_sku
            new_rows.append(new_row)


    with open(csv_path, 'w') as csv_output:
        writer = csv.writer(csv_output)
        writer.writerows(new_rows)

def ingest_via_ingestsh(selects_folder_path):
    #This works! need to add a literal zm ingest call to get ingest stdout
    proc = subprocess.Popen(['ingest.sh', selects_folder_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while proc.poll() is None:
        line = proc.stdout.readline()
        if line:
            print("\033[37m>>>{}\033[0m".format(line.strip()))


def print_progress_bar(selects_folder_path, arg_list, input_complete_length, bar_display_length):

    python_call = ['python', 'fake_input.py']
    spinner = Spinner()
    current_progress = 0
    proc = subprocess.Popen(arg_list, cwd='{}/..'.format(selects_folder_path), stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=0)
    uploaded_filenames = []
    while proc.poll() is None:
        line = proc.stdout.readline().decode()
        if line and re.match(r'\w*\sDone', line, re.I):
            file_name = re.search(r'(?P<filename>\d+_\w+\d?.jpg)', line, re.I)
            uploaded_filenames.append(file_name)
            current_progress += 1
            percent_complete = int(float(current_progress)/float(input_complete_length) * 100)
            progress_bar_now = math.floor((bar_display_length * 0.01) * percent_complete)
            progress_bar_viz = '\033[42m{}\033[00m{}\n'.format('|' * int(progress_bar_now), '_' * (bar_display_length - int(progress_bar_now))) * 3
            #progress_bar_viz = '{}{}'.format('|' * current_progress, '_' * (bar_display_length - current_progress))
            spinner_viz = spinner.update_spinner()
            final_output = '[{}]\n{}/{} {}%\n{}'.format(spinner_viz, current_progress, input_complete_length, percent_complete, progress_bar_viz)
            clear_screen()
            print(final_output)
            #print("\033[37m{}\033[0m".format(line.strip()))

def direct_ingest(
        selects_folder_path,
        environment,
        csv_path,
        selects_folder_name):

    print('ingestion started')
    message = 'studio ingestion 09/08/17'
    destination_path = "/Studio Transfer/Product/FIFO/"
    num_of_files = len(PROCESSED_FILE_NAMES)

    arg_list = [
        'zm',
        '-s',
        environment,
        'import',
        '-csv',
        '-mf',
        csv_path,
        '-d',
        destination_path,
        '-m',
        message,
        '{}/.'.format(selects_folder_name)
    ]

    print_progress_bar(selects_folder_path, arg_list, num_of_files, 80)
    #import_proc = subprocess.Popen(arg_list, cwd='{}/..'.format(selects_folder_path))
    #print("\033[37;42mINGEST COMPLETE{}\033[0m".format(('\n' + ' ' * 15) * 5))




    sys.exit()

def check_selects_folder(
        csv_names,
        processed_names,
        selects_folder_path
    ):
    """finds the difference between the photoshoot app's CSV file skus and the processed skus.
    prints the difference to the screen so that they can be found and processed correctly
    prompts the user to re-scan after fixing errors to verify nothing is still missing.
    """
    print('checking {}'.format(selects_folder_path))
    not_processed = set(csv_names) - set(processed_names)
    named_wrong = set(sku for sku in processed_names if sku[-1] == "g") - set(csv_names)

    if not not_processed:

        print("\033[32mNo Missing Files!\033[0m")
        return True
        #subprocess.call(['ingest.sh', SELECTS_FOLDER_PATH])
        #ingest_via_ingestsh(selects_folder_path)
        #the empty new lines are included so you can see if the script has completed ingestion from across the room
        #print("\033[37;42mINGEST COMPLETE{}\033[0m".format(('\n' + ' ' * 15) * 5))
        #sys.exit()
    else:
        print('\033[31mThe folowing files are missing:\033[0m')
        for file_name in not_processed:
            print('\033[31m{}\033[0m'.format(file_name))

        if named_wrong:
            print('\n\033[34mThe following files don\'t belong in the SELECTS folder\033[0m')
            for file_name in named_wrong:
                print('\033[34m{}\033[0m'.format(file_name))

    user_continue = raw_input("Press return to scan again, or enter QUIT to exit: ")

    if user_continue.lower() == 'quit':
        print("\033[32mEOD process ended\033[0m")
    else:
        recheck_sv_file_names = open_csv(METADATA_PATH)
        recheck_processed_file_names = load_file_names(SELECTS_FOLDER_PATH)
        check_selects_folder(recheck_sv_file_names, recheck_processed_file_names, selects_folder_path)


clear_screen()

ARG_PATH = parse_the_args()
SELECTS_FOLDER_PATH, METADATA_PATH, SELECTS_FOLDER_STRING = parse_paths(ARG_PATH)

CSV_FILE_NAMES = open_csv(METADATA_PATH)
PROCESSED_FILE_NAMES = load_file_names(SELECTS_FOLDER_PATH)

update_csv(METADATA_PATH, SELECTS_FOLDER_PATH)

DAM = VmLogin('username', 'password', 'environment')
DAM.authenticate()

if check_selects_folder(CSV_FILE_NAMES, PROCESSED_FILE_NAMES, SELECTS_FOLDER_PATH):
    direct_ingest(SELECTS_FOLDER_PATH, 'environment', METADATA_PATH, SELECTS_FOLDER_STRING)
    sys.exit()