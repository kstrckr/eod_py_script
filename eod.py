#! /usr/bin/python

import csv
import os, sys

selects_folder = raw_input('paste SELECTS folder name here: >>  ')

metadata_csv_path = './{}/photoshoot_{}_metadata.csv'.format(selects_folder, selects_folder[-13:-8])

# print(metadata_csv_path)

with open(metadata_csv_path, 'rb') as input:
    reader = csv.reader(input)
    photoshoot_app_skus = list(reader)

del photoshoot_app_skus[0]

skus_from_photo_app = [sku[0] for sku in photoshoot_app_skus]

path = './{}'.format(selects_folder)
dirs = os.listdir(path)

processed_file_names = [file for file in dirs]

not_processed = set(skus_from_photo_app) - set(processed_file_names)
named_wrong = set(processed_file_names) - set(skus_from_photo_app)

for file_name in not_processed:
    print file_name
# print '/n' * 3
# print named_wrong