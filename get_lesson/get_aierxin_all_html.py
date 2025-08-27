import csv
import requests
import os

csv_file = "./lesson_links.csv"
save_folder = "./每一页的html/"
os.makedirs(save_folder, exist_ok=True)

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
}

cookies = {
    "client_id": "57590606",
    "thinkphp_show_page_trace": "0|0",
    "PHPSESSID": "74f62d8798fcf01ee3a7c39713e77a9b",
    "53gid2": "13981254290000",
    "53gid0": "13981254290000",
    "53gid1": "13981254290000",
    "53revisit": "1756257536538",
    "53kf_72440321_from_host": "www.aierxin.cn",
    "uuid_53kf_72440321": "ab54ac96e496ad6ffaca9f82203d8f00",
    "53kf_72440321_land_page": "https%253A%252F%252Fwww.aierxin.cn%252F",
    "kf_72440321_land_page_ok": "1",
    "53uvid": "1",
    "onliner_zdfq72440321": "0",
    "visitor_type": "old",
    "uniqueVisitorId": "11f3a665-10d7-c507-4455-e8c79a47d409",
    "53kf_72440321_keyword": "https://www.baidu.com/link?url=ltqHt_sJcPUHED9MGiGFROIB-PyDAkbEjBDom70iKBu&wd=&eqid=d3b60937001f314f0000000468aed995",
}

with open(csv_file, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    csv_headers = next(reader)  # 跳过表头

    for row in reader:
        file_name = row[0] + "——————" + row[1]  # 文件名
        url = row[2]  # URL 列
        if not url:
            continue  # 没有 URL 跳过

        try:
            resp = requests.get(url, headers=headers, cookies=cookies, timeout=10)
            resp.raise_for_status()
            save_path = os.path.join(save_folder, file_name + ".html")
            with open(save_path, "w", encoding="utf-8") as f_html:
                f_html.write(resp.text)
            print(f"{file_name}.html 已下载")
        except Exception as e:
            print(f"下载 {url} 失败：{e}")
