import re
import os
from bs4 import BeautifulSoup
from zipfile import ZipFile

# 打开epub文件
epub_path = r"C:\Users\Crimone\西游补.epub"
output_epub_path = 'new_book.epub'
temp_folder = 'temp'

# 创建临时文件夹
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

# 解压EPUB文件到临时文件夹
with ZipFile(epub_path, 'r') as epub:
    epub.extractall(temp_folder)

# 遍历解压后的文本文件
for root, dirs, files in os.walk(temp_folder):
    for file_name in files:
        if file_name.endswith('.xhtml'):
            item_path = os.path.join(root, file_name)
            with open(item_path, 'r', encoding='utf-8') as item_file:
                item_content = item_file.read()
                soup = BeautifulSoup(item_content, 'html.parser')

                # 查找所有img标签,条件是class和alt
                images = soup.find_all('img', {'class': 'qqreader-footnote', 'alt': True})

                if images:
                    body_tag = soup.find('body')
                    body_tag.append(soup.new_tag('hr'))
                index = 1
                # 遍历图片标签,替换为脚注
                for image in images:
                    footnote_text = image['alt']
                    footnote_src = image['data-src']

                    # 创建脚注链接标签
                    a_tag = soup.new_tag('a', href=f"#footnote_{index}", id=f"footnote_link_{index}")
                    sup_tag = soup.new_tag('sup')
                    sup_tag.string = f"[{index}]"
                    a_tag.append(sup_tag)

                    # 在img标签后插入脚注链接标签
                    image.replace_with(a_tag)

                    # 创建脚注内容标签
                    footnote_tag = soup.new_tag('div', **{'class': 'footnote', 'id': f'footnote_{index}'})
                    a_tag = soup.new_tag('a', href=f"#footnote_link_{index}")
                    a_tag.string = f"[{index}]"
                    footnote_tag.append(a_tag)
                    footnote_tag.append(f"{footnote_text}")
                    body_tag = soup.find('body')
                    body_tag.append(footnote_tag)  # 将脚注内容添加到文档末尾

                    index += 1  # 递增脚注索引

                # 更新文本内容
                item_content = str(soup)

            # 替换原始文本内容并保存
            with open(item_path, 'w', encoding='utf-8') as modified_item:
                modified_item.write(item_content)

# 重新打包为EPUB文件
with ZipFile(output_epub_path, 'w') as new_epub:
    for root, dirs, files in os.walk(temp_folder):
        for file_name in files:
            item_path = os.path.join(root, file_name)
            new_epub.write(item_path, arcname=os.path.relpath(item_path, temp_folder))

# 删除临时文件夹及其内容
for root, dirs, files in os.walk(temp_folder, topdown=False):
    for file in files:
        os.remove(os.path.join(root, file))
    for dir in dirs:
        os.rmdir(os.path.join(root, dir))
os.rmdir(temp_folder)

print('修改完成，新EPUB文件已保存为:', output_epub_path)
