import subprocess
import sys
import shutil
import csv
import os

# CSV 文件路径
csv_file = "/Users/devjys/Desktop/WorkSpaces/get-aierxin/get_lesson/视频下载地址1.csv"

# 下载保存目录
download_dir = "./videos"
os.makedirs(download_dir, exist_ok=True)

# 检查 ffmpeg 是否安装
if not shutil.which("ffmpeg"):
    print("❌ 请先安装 ffmpeg 再运行此脚本")
    sys.exit(1)

# 读取 CSV 文件并下载
with open(csv_file, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        if len(row) < 2:
            continue  # 如果格式不对，跳过
        filename, m3u8_url = row
        # 去掉 HTML 后缀，避免文件名问题
        filename = filename.replace(".html_高清", "").replace(".html_清晰", "") + ".mp4"
        output_path = os.path.join(download_dir, filename)

        print(f"\n开始下载: {filename}")
        cmd = [
            "ffmpeg",
            "-i", m3u8_url,
            "-c", "copy",
            "-bsf:a", "aac_adtstoasc",
            output_path
        ]
        result = subprocess.run(cmd)
        if result.returncode == 0:
            print(f"✅ 下载完成: {output_path}")
        else:
            print(f"❌ 下载失败: {filename}")
