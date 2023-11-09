import os
import subprocess
import re
import json
import csv

# 获取视频长宽比
def get_display_aspect_ratio(filename):
    cmd = "ffprobe -v quiet -print_format json -show_streams"
    args = cmd.split() + [filename]
    ffprobe_output = subprocess.check_output(args).decode('utf-8')
    ffprobe_output_json = json.loads(ffprobe_output)

    for stream in ffprobe_output_json['streams']:
        if stream['codec_type'] == 'video' and 'display_aspect_ratio' in stream:
            # 将字符串分割为两个部分
            parts = stream['display_aspect_ratio'].split(':')
            
            if len(parts) != 2:
                return "无效的输入格式"
            
            try:
                # 转换为浮点数
                width = float(parts[0])
                height = float(parts[1])
            except ValueError:
                return "无效的数字"
            
            # 计算宽高比
            aspect_ratio = width / height
            
            # 计算与16:9和4:3的差异
            diff_16_9 = abs(aspect_ratio - 16/9)
            diff_4_3 = abs(aspect_ratio - 4/3)
            
            if diff_16_9 < diff_4_3:
                return "16/9"
            elif diff_16_9 > diff_4_3:
                return "4/3"
            
    return None


def check_base_name(base_path):
    if base_path == "":
        local_csv_file_path = r"G:\filelist.csv"

        # Read the CSV file locally
        with open(local_csv_file_path, "r", encoding="utf-8") as csv_file:
            csv_data = csv_file.read()

        # The rest of your code remains unchanged
        reader = csv.DictReader(csv_data.splitlines())
        file_list = list(reader)
        # 遍历文件列表
        for file_row in file_list:

            dir_name = file_row["路径"]
            file_name = file_row["名称"]
            complete_name = dir_name + '\\' + file_name
            # 构造文件的URL

            # 检查文件所在目录是否有completed.txt文件
            completed_file = dir_name + '\\' + "[SVTAV1]" + file_name
            if os.path.exists(completed_file):
                # 如果目录下有completed.txt文件，跳过当前文件
                print(f"File is already completed. Skipping...")
                continue

            # 如果目录下没有completed.txt文件，进行处理
            # 在这里添加你需要进行的操作
            print(f"Converting file {complete_name}")
            return complete_name
    else:
        return base_path



# 修改AVS文件中的输入路径
def modify_avs_file(avs_file_path, input_path):
    with open(avs_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    modified_content = re.sub(r'FFMpegSource2\(".*?"\)', 'FFMpegSource2()', content)
    modified_content = modified_content.replace('FFMpegSource2()', f'FFMpegSource2("{input_path}")')

    with open(avs_file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)

# 执行FFmpeg命令
def execute_ffmpeg_command(qtgmc_path, input_path, output_path, dar_ratio):
    ffmpeg_cmd = rf'.\ffmpeg -i {input_path} -vf "setdar=dar={dar_ratio}" -c:v libsvtav1 -preset 5 -crf 23 "{output_path}"'
    subprocess.run(ffmpeg_cmd, shell=True, check=True, cwd=qtgmc_path)

def execute_mkvmerge_command(input_file_path, output_file_name, aspect_ratio):
    data = [
        "--ui-language",
        "zh_CN",
        "--output",
        f"{os.path.join(os.path.dirname(input_file_path), '[SVTAV1]' + os.path.basename(input_file_path))}",
        "--no-video",
        "(",
        f"{input_file_path}",
        ")",
        "--no-track-tags",
        "--no-global-tags",
        "--language",
        "0:ja",
        "--aspect-ratio",
        f"0:{aspect_ratio}",
        "(",
        f"{os.path.join(os.path.dirname(input_file_path), output_file_name)}",
        ")"
    ]
    with open("temp.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
    mkvmerge_cmd = "mkvmerge @temp.json"
    subprocess.run(mkvmerge_cmd, shell=True, check=True)


# 主函数
def main():
    input_file_path = check_base_name(r"E:\视频\SARAH_BRIGHTMAN_DVD\B1_t00.mkv")  # 输入视频路径
    output_file_name = '[CONVERTING]' + os.path.basename(input_file_path) # 输出视频路径
    avs_file_path = 'qtgmc.avs'  # AVS文件路径
    qtgmc_path = r"D:\FFmpeg - QTGMC Easy v2022.12.27"

    # 获取视频长宽比
    aspect_ratio = get_display_aspect_ratio(input_file_path)

    # 修改AVS文件中的输入路径
    modify_avs_file(os.path.join(qtgmc_path, avs_file_path), input_file_path)

    # 执行FFmpeg命令
    execute_ffmpeg_command(qtgmc_path, avs_file_path, os.path.join(os.path.dirname(input_file_path), output_file_name),aspect_ratio)

    execute_mkvmerge_command(input_file_path, output_file_name, aspect_ratio)



# 调用主函数
if __name__ == '__main__':
    while(1):
        main()
