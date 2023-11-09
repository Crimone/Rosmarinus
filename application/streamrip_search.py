import os
import re
import shutil
from mutagen.mp4 import MP4
from mutagen.flac import FLAC

def get_tags_from_m4a(file_path):
    audio = MP4(file_path)
    album = audio.get('\xa9alb')
    artist = audio.get('\xa9ART')
    return album[0] if album else None, artist[0] if artist else None

def get_title_and_track_from_m4a(file_path):
    audio = MP4(file_path)
    title = audio.get('\xa9nam')
    track = audio.get('trkn')
    return title[0] if title else None, track[0][0] if track else None

def get_title_from_flac(file_path):
    audio = FLAC(file_path)
    return audio["title"][0] if "title" in audio else None

def download_with_streamrip(album, artist):
    # 开启一个子进程执行rip search命令
    #cmd = f'rip search -s deezer "{artist} - {album}"'
    cmd = f'rip search -s qobuz "{artist} - {album}"'
    os.system(cmd)

def remove_brackets_and_lower(text):
    # 删除()和[]中的内容
    text_without_brackets = re.sub(r'\(.*?\)|\[.*?\]|【.*?】', '', text.rsplit('-', 1)[0])
    
    # 将文本统一为小写
    return text_without_brackets.lower()

def sanitize_filename(filename):
    chars_to_remove = r"_' :.,!@#$%^&[]<>-~;！()（）【】；，。《》"
    for char in chars_to_remove:
        filename = filename.replace(char, "")
    return filename

def set_flac_track(file_path, track_no):
    audio = FLAC(file_path)
    audio['tracknumber'] = str(track_no)
    audio.save()

def remove_duplicate_lines(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 使用集合消除重复行，然后重新排序
    unique_lines = sorted(set(lines), key=lines.index)

    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(unique_lines)


def main(directory):
    flac_directory = r"C:\Soulseek Shared Folder"
    with open("matched_albums.txt", "a", encoding="utf-8") as output_file:
        for root, dirs, files in os.walk(directory):
            for dir in dirs:
                for file in os.listdir(os.path.join(root, dir)):
                    #if file.endswith('.m4a') and not file.startswith('[MATCHED]'):
                    if file.endswith('.m4a'):
                        file_path = os.path.join(root, dir, file)

                        m4a_title, m4a_track = get_title_and_track_from_m4a(file_path)
                        album, artist = get_tags_from_m4a(file_path)
                        if album and artist:

                            print(f"Downloading {artist} - {album}...")
                            output_file.write(f"{artist} - {album}\n")
                            
                            download_with_streamrip(album, artist)
                            matched = False
                            for flac_root, flac_dirs, flac_files in os.walk(flac_directory):
                                for flac_file in flac_files:
                                    if flac_file.endswith('.flac'):
                                        flac_path = os.path.join(flac_root, flac_file)
                                        flac_title = get_title_from_flac(flac_path)
                                        
                                        if sanitize_filename(remove_brackets_and_lower(m4a_title.replace("Album Version", ""))) == sanitize_filename(remove_brackets_and_lower(flac_title.replace("Album Version", ""))):
                                            os.rename(flac_path, os.path.join(root, dir, flac_file))
                                            os.remove(file_path)
                                            set_flac_track(os.path.join(root, dir, flac_file), m4a_track)
                                            matched = True
                                            break
                                if matched:
                                    break
                            if not matched:
                                print(f"No matching FLAC file found for {file}.")
                            
                
                # 删除所有 flac 文件
                for flac_file in os.listdir(flac_directory):
                    shutil.rmtree(os.path.join(flac_directory, flac_file))
                

if __name__ == "__main__":
    dir_path = r"C:\KKBOX Downloads"
    main(dir_path)
