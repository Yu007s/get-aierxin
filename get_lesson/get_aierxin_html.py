import requests
from bs4 import BeautifulSoup
import re

url_set = ["https://www.aierxin.cn/personalcenter/play.html?class_id=1734&type=0"
    , "https://www.aierxin.cn/personalcenter/play.html?class_id=1963&type=1"
    , "https://www.aierxin.cn/personalcenter/play.html?class_id=1731&type=1"
        , "https://www.aierxin.cn/personalcenter/play.html?class_id=1961&type=1"
           , "https://www.aierxin.cn/personalcenter/play.html?class_id=1730&type=1"
           ]

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,zh-TW;q=0.8",
    "cache-control": "max-age=0",
    "priority": "u=0, i",
    "referer": "https://www.aierxin.cn/Personalcenter/index.html",
    "sec-ch-ua": '"Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
}

cookies = {
    "client_id": "57590606",
    "thinkphp_show_page_trace": "0|0",
    "53gid2": "13981254290000",
    "53revisit": "1756257536538",
    "uniqueVisitorId": "11f3a665-10d7-c507-4455-e8c79a47d409",
    "PHPSESSID": "378039b32cb42c1e475e327dc7c40415",
    "53kf_72440321_from_host": "www.aierxin.cn",
    "uuid_53kf_72440321": "4c73cf2409027a1dd526b7a9076902d3",
    "53kf_72440321_land_page": "https%253A%252F%252Fwww.aierxin.cn%252Flogin%252Findex.html",
    "kf_72440321_land_page_ok": "1",
    "visitor_type": "old",
    "53gid0": "13981254290000",
    "53gid1": "13981254290000",
    "53kf_72440321_keyword": "https%3A%2F%2Fwww.aierxin.cn%2Flogin%2Findex.html",
    "53uvid": "1",
    "onliner_zdfq72440321": "0",
}


for url in url_set:
    # 请求页面
    resp = requests.get(url, headers=headers, cookies=cookies, timeout=10)
    resp.raise_for_status()
    html = resp.text

    # 解析 HTML
    soup = BeautifulSoup(html, "html.parser")

    # 取第一个 h4 标签内容
    first_h4 = soup.find("h4")
    if first_h4:
        title = first_h4.get_text(strip=True)
    else:
        title = "default_title"

    # 清理非法字符，避免文件名报错
    safe_title = re.sub(r'[\\/:*?"<>|]', "_", title)

    # 保存成 HTML 文件
    filename = f"./html文件/{safe_title}.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"页面已保存到 {filename}")
