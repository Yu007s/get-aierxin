import requests
import json
import re
import os
import csv

folder_path = "./每一页的html/"
output_csv = "视频下载地址.csv"

# 获取文件夹下所有 HTML 文件
file_list = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

headers = {
    "accept": "*/*",
    "accept-language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
    "referer": "https://www.aierxin.cn/",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "script",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "cross-site",
    "sec-fetch-storage-access": "none",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}

with open(output_csv, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["文件名", "下载地址"])  # 写入表头

    for f_name in file_list:
        # 读取 HTML 文件
        with open(os.path.join(folder_path, f_name), "r", encoding="utf-8") as f:
            html = f.read()

        # 正则匹配 list 数组里的第一个 vid
        match = re.search(r'var list = \[\s*"([0-9A-F]+)"\s*\];', html)
        if match:
            vid = match.group(1)
            # 构造 BokeCC 接口 URL
            url = (
                f"https://p.bokecc.com/servlet/getvideofile?"
                f"vid={vid}"
                "&siteid=606E693D99DE632E"
                "&width=100%25"
                "&useragent=other"
                "&version=20140214"
                "&hlssupport=1"
                "&vc="
                "&mediatype=1"
                "&divid=cc_video_BD5499BC21D1D5CF7E6C9CEE8B422289_5855886"
                "&customerId=app_pc_12069879271"
                "&callback=cc_jsonp_callback_819777"
                "&r=7267976.99103398"
            )

            try:
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                text = response.text

                # JSONP 去掉回调函数
                json_match = re.search(r"cc_jsonp_callback_\d+\((.*)\)", text)
                if json_match:
                    data_json = json_match.group(1)
                    data = json.loads(data_json)

                    # 遍历 copies 列表
                    for copy in data.get("copies", []):
                        desp = copy.get("desp", "")
                        playurl = copy.get("playurl", "")
                        # 去掉 .html 后缀
                        base_name = os.path.splitext(f_name)[0]

                        file_label = f"{base_name}_{desp}"
                        writer.writerow([file_label, playurl])
                else:
                    print(f"{f_name} -> 未匹配到 JSON 数据")
            except Exception as e:
                print(f"{f_name} -> 请求失败: {e}")
