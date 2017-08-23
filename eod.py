#! /usr/bin/python

import csv
import os
import sys
import subprocess

def clear_screen():
    """clears screen"""
    os.system('cls' if os.name =='nt' else 'clear')

clear_screen()

selects_folder = raw_input('drag SELECTS folder into window and press ENTER: >>  ')
selects_folder = selects_folder.strip()

metadata_csv_path = '/{}/photoshoot_{}_metadata.csv'.format(selects_folder, selects_folder[-13:-8])


# print(metadata_csv_path)

def open_csv(csv_path):
    """loads the photoshoot app's csv file, returns only a list of SKU filenames"""
    with open(csv_path, 'rb') as input:
        reader = csv.reader(input)
        photoshoot_app_skus = list(reader)
        del photoshoot_app_skus[0]
        skus_from_photo_app = [sku[0] for sku in photoshoot_app_skus]
        return skus_from_photo_app

def load_file_names(selects_path):
    """returns a list of processed filenames from the SELECTS folder"""
    path = selects_path
    dirs = os.listdir(path)
    file_names = [file for file in dirs]
    return file_names


def check_selects_folder(csv_names, processed_names):
    """finds the difference between the photoshoot app's CSV file skus and the processed skus.
    prints the difference to the screen so that they can be found and processed correctly
    prompts the user to re-scan after fixing errors to verify nothing is still missing.
    """
    not_processed = set(csv_names) - set(processed_names)
    # named_wrong = set(processed_file_names) - set(skus_from_photo_app)

    if not not_processed:
        print("\033[32mNo Errors!\033[0m")
        subprocess.call(['ingest.sh', selects_folder])
        print("\033[37;42mINGEST COMPLETE\033[0m")
        sys.exit()
    else:
        print('\033[31mThe folowing files are missing:\033[0m')
        for file_name in not_processed:
            print('\033[31m{}\033[0m'.format(file_name))
    
    user_continue = raw_input("Press return to scan again, or enter x to exit: ")

    if user_continue.lower() == 'x':
        print("\033[32mHave a GREAT day!\033[0m")
    else: 
        recheck_sv_file_names = open_csv(metadata_csv_path)
        recheck_processed_file_names = load_file_names(selects_folder)
        check_selects_folder(recheck_sv_file_names, recheck_processed_file_names)

csv_file_names = open_csv(metadata_csv_path)
processed_file_names = load_file_names(selects_folder)
check_selects_folder(csv_file_names, processed_file_names)
