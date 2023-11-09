import os
import subprocess
from mutagen.flac import FLAC
from imgbbpy.imgbb import SyncClient

def find_flac_files(directory):
    """递归查找目录下的第一个FLAC文件"""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.flac'):
                return os.path.join(root, file)
    return None

def get_flac_info(flac_file):
    """获取FLAC文件的信息"""
    audio = FLAC(flac_file)
    # 首先尝试获取'albumartist'标签，如果不存在则使用'artist'标签
    artist = audio.get('albumartist') or audio.get('artist')
    if artist:
        artist = artist[0]
    else:
        raise ValueError("No artist or album artist tag found in FLAC file.")
    album = audio.get('album')[0]
    date = audio.get('date')[0][:4]
    return artist, album, date

def rename_directory(directory, artist, album, date):
    """重命名目录"""
    new_name = f"{artist} - {album} ({date}) [FLAC]"
    parent_dir = os.path.dirname(directory)
    new_path = os.path.join(parent_dir, new_name)
    os.rename(directory, new_path)
    return new_path

def generate_spectrogram(directory):
    """生成频谱图"""
    command = 'sox *.flac -n spectrogram -o spectrogram.png'
    result = subprocess.run(command, shell=True, check=True, cwd=directory)
    return os.path.join(directory,"spectrogram.png")

def create_torrent(torrent_directory, transmission_directory, directory):
    """创建种子文件"""
    torrent_file = os.path.join(torrent_directory, os.path.basename(directory) + '.torrent')
    command = rf'{os.path.join(transmission_directory, "transmission-create")} -p -t https://tracker.open.cd/announce.php -o "{torrent_file}" "{directory}"'
    subprocess.run(command)
    return torrent_file

def list_directories(directory):
    # 获取所有条目
    entries = os.listdir(directory)
    subdirs = [d for d in entries if os.path.isdir(os.path.join(directory, d))]
    
    if subdirs:
        print("Subdirectories:")
        for subdir in subdirs:
            print(subdir)
            spectrogram_image = generate_spectrogram(subdir)
            print(f"Spectrogram generated: {spectrogram_image}")
    else:
        print("Current Directory:")
        print(os.path.basename(directory))
        spectrogram_image = generate_spectrogram(subdir)
        print(f"Spectrogram generated: {spectrogram_image}")

# 主执行函数
def process_music_folder(torrent_directory,transmission_directory, directory):
    # 找到第一个FLAC文件
    flac_file = find_flac_files(directory)
    if not flac_file:
        print("No FLAC files found in the directory.")
        return

    # 获取FLAC文件信息
    artist, album, date = get_flac_info(flac_file)

    # 重命名目录
    #directory = rename_directory(directory, artist, album, date)

    # 生成频谱图
    list_directories(directory)

    # 创建种子文件
    torrent_file = create_torrent(torrent_directory,transmission_directory, directory)
    print(f"Torrent created: {torrent_file}")

# 假定当前目录为目标目录
current_directory = os.getcwd()
torrent_directory = r"C:\Users\Crimone"
transmission_directory = r"D:\Transmission"
process_music_folder(torrent_directory, transmission_directory, str(current_directory))
