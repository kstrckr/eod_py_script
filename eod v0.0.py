import csv
import os, sys

selects_folder = raw_input('paste SELECTS folder name here: >>  ')

with open('10592_metadata_original.csv', 'rb') as input:
    reader = csv.reader(input)
    list = list(reader)

skus_from_photo_app = []

for sku in list:
    skus_from_photo_app.append(sku[0])

# print skus_from_photo_app

path = './{}'.format(selects_folder)
dirs = os.listdir(path)

processed_file_names = []

for file in dirs:
    processed_file_names.append(file)

# print '\n'*3
# print processed_file_names

not_processed = set(skus_from_photo_app) - set(processed_file_names)
named_wrong = set(processed_file_names) - set(skus_from_photo_app)

for file_name in not_processed:
    print file_name
# print '/n' * 3
# print named_wrong