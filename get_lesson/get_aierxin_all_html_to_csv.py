import csv
from bs4 import BeautifulSoup
import os

folder_path = "./html文件/"
csv_file = "./lesson_links.csv"

# 获取文件夹下所有文件（不包括子目录）
file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

print("文件列表：")
for f_name in file_list:
    print(f_name)

# 打开 CSV 文件一次，写入表头
with open(csv_file, "w", encoding="utf-8", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["文件夹名", "内容", "URL"])  # 增加文件名列

    # 遍历所有 HTML 文件
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)

        # 读取 HTML
        with open(file_path, "r", encoding="utf-8") as html_file:
            html = html_file.read()

        soup = BeautifulSoup(html, "html.parser")

        # 找到所有指定 style 的标签
        tags = soup.find_all(attrs={"style": "color: #fff;overflow: hidden"})

        base_name = os.path.splitext(file_name)[0]
        # 写入每个标签的内容和 URL
        for tag in tags:
            content = tag.get_text(strip=True)
            url = tag.get("href") or tag.get("src") or ""
            writer.writerow([base_name, content, url])

print(f"提取完成，结果已保存到 {csv_file}")
