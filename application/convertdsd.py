import os
import subprocess
import glob
import argparse
import json
from termcolor import colored
from mutagen.dsf import DSF
from mutagen.wavpack import WavPack
from mutagen.apev2 import APEv2

def migrate_tags(source_file, target_file):
    source_tags = DSF(source_file)
    target_tags = WavPack(target_file)

        # 将标签信息转换为字典
    id3_tags = {}
    for item in source_tags.items():
        # 将标签名从字节转换为字符串
        tag_name = item[0]
        # 将标签值从字节转换为字符串
        tag_value = item[1]
        
        # 将标签名和标签值添加到字典中
        id3_tags[tag_name] = tag_value
    
    # 将ID3标签导出为JSON文件
    with open("json_file.json", 'w') as f:
        json.dump(id3_tags, f, indent=4)


    for key, value in source_tags.items():
        target_tags[key] = value

    target_tags.save()

def compress_dsf_files(path,delete_source):
    dsf_files = glob.glob(os.path.join(glob.escape(path), '**\\*.dsf'), recursive=True)

    for dsf_file in dsf_files:
        wv_file = os.path.splitext(dsf_file)[0] + '.wv'

        if os.path.exists(wv_file):
            print(f'Skipping {dsf_file} - .wv file already exists')
            continue

        print(colored(f'Compressing {dsf_file} to .wv file',"green"))
        wavpack_cmd = rf'wavpack -h -m --import-id3 -r "{dsf_file}"'
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
