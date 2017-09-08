import subprocess

def direct_ingest(
    selects_folder_path,
    environment,
    csv_path,
    message,
    selects_folder_name):

    destination_path = "/Product/FIFO/"

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

    subprocess.call(['cd', selects_folder_path])
    subprocess.call(arg_list)