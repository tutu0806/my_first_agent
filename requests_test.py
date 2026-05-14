import requests
import json

# 1. 最简单 GET 请求
url = "https://httpbin.org/get"
res = requests.get(url)
res_data = res.json()
print("GET请求结果：", res_data["origin"])

# 2. POST 请求（模拟大模型API调用）
url_post = "https://httpbin.org/post"
headers = {"Content-Type": "application/json"}
payload = {
    "model": "chat",
    "prompt": "你好，介绍下AI Agent",
    "temperature": 0.7
}

res2 = requests.post(url_post, headers=headers, data=json.dumps(payload))
result = res2.json()
print("\nPOST请求返回：")
print(result["json"])