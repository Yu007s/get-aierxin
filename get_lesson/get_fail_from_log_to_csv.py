import re
import csv

# 日志文件路径
log_file_path = '/Users/devjys/Desktop/WorkSpaces/get-aierxin/get_lesson/下载日志.log'
# 源CSV文件路径
csv_file_path = '/Users/devjys/Desktop/WorkSpaces/get-aierxin/get_lesson/视频下载地址.csv'
# 输出的新CSV文件路径
output_file_path = '/Users/devjys/Desktop/WorkSpaces/get-aierxin/get_lesson/失败文件下载地址.csv'

# 正则表达式
pattern = r'❌ 下载失败: (.*?), 错误'


def extract_failed_files(log_file_path):
    failed_files = []
    with open(log_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                file_name = match.group(1).replace('.mp4', '')  # 去掉 .mp4 后缀
                failed_files.append(file_name)
    return failed_files


def filter_csv_by_failed_files(csv_file_path, failed_files, output_file_path):
    matched_rows = []

    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row:  # 跳过空行
                continue
            first_col = row[0]
            # 检查 CSV 第一列是否以失败文件名开头
            if any(first_col.startswith(f) for f in failed_files):
                matched_rows.append(row)

    # 写入新文件
    with open(output_file_path, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(matched_rows)


if __name__ == "__main__":
    failed_files = extract_failed_files(log_file_path)
    if failed_files:
        print("找到失败的文件名：")
        for f in failed_files:
            print(f)
        filter_csv_by_failed_files(csv_file_path, failed_files, output_file_path)
        print(f"\n已将匹配的行写入: {output_file_path}")
    else:
        print("没有找到下载失败的文件。")
