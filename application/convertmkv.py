import os
import subprocess
import re
import json

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

# 修改AVS文件中的输入路径
def modify_avs_file(avs_file_path, input_path):
    with open(avs_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    modified_content = re.sub(r'FFMpegSource2\(".*?"\)', 'FFMpegSource2()', content)
    modified_content = modified_content.replace('FFMpegSource2()', f'FFMpegSource2("{input_path}")')

    with open(avs_file_path, 'w', encoding='utf-8') as file:
        file.write(modified_content)

# 执行FFmpeg命令
def execute_ffmpeg_command(input_path, output_path, dar_ratio):
    ffmpeg_cmd = rf'.\ffmpeg -i {input_path} -vf "setdar=dar={dar_ratio}" -c:v libsvtav1 -preset 5 -crf 23 "{output_path}"'
    subprocess.run(ffmpeg_cmd, shell=True, check=True, cwd=r"C:\Users\Crimone\Downloads\FFmpeg - QTGMC Easy v2022.12.27\FFmpeg - QTGMC Easy v2022.12.27")

def execute_mkvmerge_command(input_file_path, output_file_name, aspect_ratio):
    data = [
        "--ui-language",
        "zh_CN",
        "--output",
        f"{os.path.join(os.path.dirname(input_file_path), '[SVTAV1]' + os.path.basename(input_file_path))}",
        "--no-audio",
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
        "--language",
        "1:ja",
        "(",
        f"{os.path.join(os.path.dirname(input_file_path), output_file_name)}",
        ")",
        "--track-order",
        "1:0,1:1"
    ]
    with open("temp.json", 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
    mkvmerge_cmd = "mkvmerge @temp.json"
    subprocess.run(mkvmerge_cmd, shell=True, check=True)


# 主函数
def main():
    input_file_path = r"L:\Soulseek Downloads\Soulseek Shared Folder\久保田早紀 - Saki Kubota PREMIUM\DISC-8 - フェアウエル・コンサート (Original Remastered 2019)\久保田早紀 フェアウェル コンサート 1984 Saki Kubota Farewell Concert [VwXP16G06Os].mkv"  # 输入视频路径
    output_file_name = 'output_video.mkv'  # 输出视频路径
    avs_file_path = 'qtgmc.avs'  # AVS文件路径
    qtgmc_path = r"C:\Users\Crimone\Downloads\FFmpeg - QTGMC Easy v2022.12.27\FFmpeg - QTGMC Easy v2022.12.27"

    # 获取视频长宽比
    aspect_ratio = get_display_aspect_ratio(input_file_path)

    # 修改AVS文件中的输入路径
    modify_avs_file(os.path.join(qtgmc_path, avs_file_path), input_file_path)

    # 执行FFmpeg命令
    execute_ffmpeg_command(avs_file_path, os.path.join(os.path.dirname(input_file_path), output_file_name),aspect_ratio)

    execute_mkvmerge_command(input_file_path, output_file_name, aspect_ratio)



# 调用主函数
if __name__ == '__main__':
    main()
