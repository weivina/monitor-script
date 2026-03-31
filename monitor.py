import requests
import json
import os

URL = "https://m.client.10010.com/servicequerybusiness/queryTariffNew/operateData/e7ca7fd5ae8e49a3ba0d18bedf67ec99"

# PushPlus Token（你提供的）
PUSH_TOKEN = "1e8e8597e2444a89ac33d662cb027908"

def send(msg):
    try:
        requests.post(
            "http://www.pushplus.plus/send",
            json={
                "token": PUSH_TOKEN,
                "title": "联通套餐变动",
                "content": msg
            }
        )
    except Exception as e:
        print("推送失败:", e)

def clean_data(data):
    # 删除 timeStr，避免误报
    data.pop("timeStr", None)
    return data

def main():
    res = requests.get(URL)
    data = res.json()

    data = clean_data(data)

    # 转成字符串用于对比（排序避免误判）
    new = json.dumps(data, sort_keys=True, ensure_ascii=False)

    # 读取旧数据
    old = ""
    if os.path.exists("data.txt"):
        with open("data.txt", "r", encoding="utf-8") as f:
            old = f.read()

    # 判断变化
    if old and new != old:
        send("检测到套餐内容发生变化，请及时查看！")

    # 保存新数据
    with open("data.txt", "w", encoding="utf-8") as f:
        f.write(new)

if __name__ == "__main__":
    main()
