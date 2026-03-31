import requests
import json
import os

print("开始运行")

URL = "https://m.client.10010.com/servicequerybusiness/queryTariffNew/operateData/e7ca7fd5ae8e49a3ba0d18bedf67ec99"

# 从 GitHub Secrets 读取
PUSH_TOKEN = os.getenv("SCKEY")

def send(msg):
    if not PUSH_TOKEN:
        print("没有推送token")
        return

    try:
        res = requests.post(
            "http://www.pushplus.plus/send",
            json={
                "token": PUSH_TOKEN,
                "title": "联通套餐变动",
                "content": msg
            },
            timeout=10
        )
        print("推送结果:", res.text)
    except Exception as e:
        print("推送失败:", e)

def clean_data(data):
    # 删除 timeStr，避免误报
    if isinstance(data, dict):
        data.pop("timeStr", None)
    return data

def get_data():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://m.client.10010.com/",
        "Accept": "application/json"
    }

    res = requests.get(URL, headers=headers, timeout=10)
    print("状态码:", res.status_code)

    if res.status_code != 200:
        raise Exception(f"请求失败: {res.status_code}")

    return res.json()

def main():
    try:
        data = get_data()
        data = clean_data(data)

        new = json.dumps(data, sort_keys=True, ensure_ascii=False)

    except Exception as e:
        print("获取数据失败:", e)
        return

    old = ""
    if os.path.exists("data.txt"):
        try:
            with open("data.txt", "r", encoding="utf-8") as f:
                old = f.read()
        except:
            print("读取旧数据失败")

    if old:
        if new != old:
            print("检测到变化")
            send("检测到套餐内容发生变化，请及时查看！")
        else:
            print("无变化")
    else:
        print("首次运行，初始化数据")

    try:
        with open("data.txt", "w", encoding="utf-8") as f:
            f.write(new)
        print("写入 data.txt 成功")
    except Exception as e:
        print("写入失败:", e)

if __name__ == "__main__":
    main()
