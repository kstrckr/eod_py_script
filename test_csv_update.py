import csv

def update_csv(csv_metadata_path)

    new_rows = []

    with open (csv_metadata_path, 'r') as csv_data:
        reader = csv.reader(csv_data)
        header = reader.next()
        new_rows.append(header)
        
        for row in reader:
            new_row = row
            new_sku = "BOOM{}".format(row[0])
            new_row[0] = new_sku
            new_rows.append(new_row)


    with open (csv_metadata_path, 'w') as csv_output:
        writer = csv.writer(csv_output)
        writer.writerows(new_rows)