#! /usr/bin/python

#! /usr/bin/python

import csv
import os, sys
import subprocess

selects_folder = raw_input('paste SELECTS folder name here: >>  ')

metadata_csv_path = '/{}/photoshoot_{}_metadata.csv'.format(selects_folder, selects_folder[-13:-8])


# print(metadata_csv_path)

def open_csv(csv_path):
    with open(csv_path, 'rb') as input:
        reader = csv.reader(input)
        photoshoot_app_skus = list(reader)
        del photoshoot_app_skus[0]
        skus_from_photo_app = [sku[0] for sku in photoshoot_app_skus]
        return skus_from_photo_app

def load_file_names(selects_path):
    path = '{}'.format(selects_path)
    dirs = os.listdir(path)
    file_names = [file for file in dirs]
    return file_names


def check_selects_folder(csv_names, processed_names):
    not_processed = set(csv_names) - set(processed_names)
    # named_wrong = set(processed_file_names) - set(skus_from_photo_app)

    if not len(not_processed):
        print("No Errors!")
        subprocess.call(['ingest.sh', selects_folder])
        #break
    else:
        for file_name in not_processed:
            print(file_name)
    
    user_continue = raw_input("Press return to scan again, or enter x to exit: ")

    if user_continue.lower() == 'x':
        print("thanks!")
    else: 
        recheck_sv_file_names = open_csv(metadata_csv_path)
        recheck_processed_file_names = load_file_names(selects_folder)
        check_selects_folder(recheck_sv_file_names, recheck_processed_file_names)

csv_file_names = open_csv(metadata_csv_path)
processed_file_names = load_file_names(selects_folder)
check_selects_folder(csv_file_names, processed_file_names)

# print '/n' * 3
# print named_wrong