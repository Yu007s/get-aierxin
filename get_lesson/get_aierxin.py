import subprocess
import sys
import shutil
import csv
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import time

# CSV 文件路径
csv_file = "/Users/devjys/Desktop/WorkSpaces/get-aierxin/get_lesson/失败文件下载地址.csv"

# 下载保存目录
download_dir = "./videos"
os.makedirs(download_dir, exist_ok=True)

# 最大同时下载线程数
MAX_WORKERS = 20

# 检查 ffmpeg 是否安装
if not shutil.which("ffmpeg"):
    print("❌ 请先安装 ffmpeg 再运行此脚本")
    sys.exit(1)


# 下载任务函数
def download_video(task):
    filename, m3u8_url = task
    # 去掉 HTML 后缀，避免文件名问题
    filename = filename + ".mp4"
    output_path = os.path.join(download_dir, filename)

    print(f"\n开始下载: {filename}")
    cmd = [
        "ffmpeg",
        "-i", m3u8_url,
        "-c", "copy",
        "-bsf:a", "aac_adtstoasc",
        output_path
    ]

    try:
        # 使用subprocess.run执行命令，设置超时时间为2小时
        result = subprocess.run(cmd, timeout=7200, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ 下载完成: {output_path}")
            return True, filename
        else:
            print(f"❌ 下载失败: {filename}, 错误: {result.stderr}")
            return False, filename
    except subprocess.TimeoutExpired:
        print(f"❌ 下载超时: {filename}")
        return False, filename
    except Exception as e:
        print(f"❌ 下载异常: {filename}, 错误: {str(e)}")
        return False, filename


# 读取 CSV 文件并创建任务列表
def read_tasks_from_csv():
    tasks = []
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 2:
                continue  # 如果格式不对，跳过
            filename, m3u8_url = row
            tasks.append((filename, m3u8_url))
    return tasks


# 主函数
def main():
    # 读取所有任务
    tasks = read_tasks_from_csv()
    total_tasks = len(tasks)

    if total_tasks == 0:
        print("没有找到需要下载的任务")
        return

    print(f"找到 {total_tasks} 个下载任务，使用 {MAX_WORKERS} 个线程同时下载")

    # 使用线程池执行下载任务
    completed = 0
    failed = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        # 提交所有任务
        future_to_task = {executor.submit(download_video, task): task for task in tasks}

        # 处理完成的任务
        for future in as_completed(future_to_task):
            task = future_to_task[future]
            try:
                success, filename = future.result()
                if success:
                    completed += 1
                else:
                    failed += 1

                print(f"进度: {completed + failed}/{total_tasks} | 成功: {completed} | 失败: {failed}")
            except Exception as exc:
                failed += 1
                print(f'任务 {task[0]} 生成异常: {exc}')
                print(f"进度: {completed + failed}/{total_tasks} | 成功: {completed} | 失败: {failed}")

    print(f"\n所有任务完成! 成功: {completed}, 失败: {failed}")


if __name__ == "__main__":
    main()