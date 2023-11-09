import os
import subprocess
import glob
import argparse
import csv
from termcolor import colored


def compress_dsf_files(path,delete_source):
    while 1:
        extname = "png"
        everything_cmd = rf'D:\Everything\es -sort-size-descending -size -export-csv "D:\source\repos\rosmarinus\application\png.csv" "I:\" ".{extname}"'
        subprocess.run(everything_cmd, shell=True, check=True)

        local_csv_file_path = r"D:\source\repos\rosmarinus\application\png.csv"

        # Read the CSV file locally
        with open(local_csv_file_path, "r", encoding="utf-8") as csv_file:
            csv_data = csv_file.read()

        # The rest of your code remains unchanged
        reader = csv.DictReader(csv_data.splitlines())
        file_list = list(reader)

        size = file_list[0]["Size"]
        file_name = file_list[0]["Filename"]
        file_path = os.path.dirname(file_name)

        if int(size) < 20*1024*1024:
            break

        print(colored(f'Now Compressing directory {file_path}',"cyan"))

        dsf_files = glob.glob(os.path.join(glob.escape(file_path), f'**\\*.{extname}'), recursive=True)

        for dsf_file in dsf_files:
            wv_file = os.path.splitext(dsf_file)[0] + '.webp'

            if os.path.exists(wv_file):
                print(f'Skipping {dsf_file} - .wv file already exists')
                continue

            print(colored(f'Compressing {dsf_file} to .wv file',"green"))
            wavpack_cmd = rf'magick "{dsf_file}" -quality 80 "{wv_file}"'
            subprocess.run(wavpack_cmd, shell=True, check=True)

        print(colored(f'All compression is complete!',"green"))

        for dsf_file in dsf_files:
            if delete_source:
                os.remove(dsf_file)
                print(colored(f'Deleted {dsf_file}',"blue"))

def main():
    parser = argparse.ArgumentParser(description='Compress dsf files to wv files')
    parser.add_argument('-d', '--delete', action='store_true', help='Delete source files after conversion')
    parser.add_argument('path', help='The path to the directory containing dsf files')

    args = parser.parse_args()

    path = args.path
    delete_source = args.delete

    if delete_source:
        print(colored(f'Notice: The source files will be deleted after conversion!', 'red'))

    if os.path.isfile(path):
        path = os.path.dirname(path)

    compress_dsf_files(path,delete_source)


if __name__ == '__main__':
    main()


