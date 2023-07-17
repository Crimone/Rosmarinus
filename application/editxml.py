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

# 使用示例
path = r"K:\KOTOKO Anime song’s complete album “The Fable”\KOTOKO - KOTOKO Anime song’s complete album “The Fable” (2020) {GNCA-1591} [FLAC]\KOTOKO 「The Fable」 特典"

update_chapter_string(path+"\\1.xml", path+"\\1.txt")