#! /usr/bin/python

#Kurt Strecker
#kstrecker@gilt.com
# v0.8 - 8/24/2017

import csv
import os
import sys
import subprocess
import argparse
import glob

def clear_screen():
    """clears the screen"""
    os.system('cls' if os.name =='nt' else 'clear')

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
        selects_folder = path_arg.strip()
    else:
        print('type QUIT to exit or,')
        selects_folder = raw_input('drag SELECTS folder into window and press ENTER: >>  ')
        if selects_folder.lower() == 'quit':
            exit()
        elif not selects_folder:
            clear_screen()
            print("must drag SELECTS folder into window or type QUIT to exit\n\n")
            parse_paths()
        selects_folder = selects_folder.strip()

    metadata_csv_path = '/{}/photoshoot_{}_metadata.csv'.format(
        selects_folder, selects_folder[-13:-8])

    return (selects_folder, metadata_csv_path)

# print(metadata_csv_path)

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

def ingest_via_ingestsh(selects_folder_path):
    #This works! need to add a literal zm ingest call to get ingest stdout
    proc = subprocess.Popen(['ingest.sh', selects_folder_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while proc.poll() is None:
        line = proc.stdout.readline()
        if line:
            print("\033[37m>>>{}\033[0m".format(line.strip()))

def check_selects_folder(csv_names, processed_names, selects_folder_path):
    """finds the difference between the photoshoot app's CSV file skus and the processed skus.
    prints the difference to the screen so that they can be found and processed correctly
    prompts the user to re-scan after fixing errors to verify nothing is still missing.
    """
    print('checking {}'.format(selects_folder_path))
    not_processed = set(csv_names) - set(processed_names)
    named_wrong = set(sku for sku in processed_names if sku[-1] == "g") - set(csv_names)

    if not not_processed:
        print("\033[32mNo Missing Files!\033[0m")
        #subprocess.call(['ingest.sh', SELECTS_FOLDER_PATH])
        ingest_via_ingestsh(selects_folder_path)
        #the empty new lines are included so you can see if the script has completed ingestion from across the room
        print("\033[37;42mINGEST COMPLETE{}\033[0m".format(('\n' + ' ' * 15) * 5))
        sys.exit()
    else:
        print('\033[31mThe folowing files are missing:\033[0m')
        for file_name in not_processed:
            print('\033[31m{}\033[0m'.format(file_name))

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
SELECTS_FOLDER_PATH, METADATA_PATH = parse_paths(ARG_PATH)

CSV_FILE_NAMES = open_csv(METADATA_PATH)
PROCESSED_FILE_NAMES = load_file_names(SELECTS_FOLDER_PATH)
check_selects_folder(CSV_FILE_NAMES, PROCESSED_FILE_NAMES, SELECTS_FOLDER_PATH)
