import os
import subprocess
from lxml import etree
    
def update_chapter_string(xml_file, txt_file):
    # 读取txt文件中的标题信息
    with open(txt_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 打开xml文件并解析为XML树
    tree = etree.parse(xml_file)
    root = tree.getroot()

    # 获取ChapterString节点，并根据txt文件中的标题信息进行修改
    chapter_string_nodes = root.findall('.//ChapterString')
    for i, node in enumerate(chapter_string_nodes):
        if i < len(lines):
            node.text = lines[i].strip()

    # 保存修改后的XML文件
    tree.write(xml_file, encoding='utf-8', xml_declaration=True)

def update_mkv_chapter_titles(mkv_file_path, txt_file_path):
    # First, extract the chapters to a temporary XML file
    temp_xml_file = "temp.xml"
    subprocess.run(["mkvextract", mkv_file_path, "chapters", temp_xml_file])

    # Read the XML file and replace the chapter titles
    update_chapter_string(temp_xml_file, txt_file_path)

    # Use mkvpropedit to update the MKV file with the new chapter titles
    subprocess.run(["mkvpropedit", mkv_file_path, "--chapters", temp_xml_file])

    # Remove the temporary XML file
    os.remove(temp_xml_file)

# Example usage:
path = r"J:\Live Video\NieR-Orchestra Concert 12018\NieR-Orchestra Concert 12018.mkv"

txt = r"application\chapter.txt"

update_mkv_chapter_titles(path, txt)