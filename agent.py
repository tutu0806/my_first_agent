import requests
import json
from datetime import datetime

#定义计算器函数，获取时间函数，城市天气列表
def calculate(expression):
    try:
        return str(eval(expression.strip()))
    except:
        return "计算失败，请输入正确算式"

def get_now_time():
    now = datetime.now()
    return now.strftime("当前时间：%Y年%m月%d日 %H:%M:%S")

def get_weather(city):
    weather_data = {
        "北京": "晴，25℃",
        "上海": "多云，28℃",
        "广州": "小雨，30℃",
        "深圳": "雷阵雨，31℃",
        "东莞": "多云，27℃"
    }
    return weather_data.get(city, f"暂未收录{city}的天气")

# 调用ollama端口
url = "http://localhost:11434/api/chat"
#给助手定位
messages = [
    {"role": "system", "content": "你是一个友好的AI助手，回答简洁明了。"}
]

print("=== 🤖 半自动工具Agent已启动 ===")
print("你可以直接说：\n- 帮我算 1+1\n- 现在几点了\n- 东莞天气\n输入 exit 退出\n")
#判断是否退出对话
while True:
    user_input = input("你：")
    if user_input.lower() == "exit":
        print("Agent：再见！")
        break

    # 手动触发工具（简单粗暴但稳定）
    if user_input.startswith("帮我算"):
        expr = user_input[4:]  # 提取算式
        result = calculate(expr)
        print(f"Agent：{expr} 的结果是 {result}")
        continue
    elif "几点了" in user_input or "时间" in user_input:
        print(f"Agent：{get_now_time()}")
        continue
    elif "天气" in user_input:
        # 提取城市名（简单匹配）
        city = None
        for name in ["北京", "上海", "广州", "深圳", "东莞"]:
            if name in user_input:
                city = name
                break
        if city:
            print(f"Agent：{city}的天气是 {get_weather(city)}")
        else:
            print("Agent：请告诉我具体城市名，比如“东莞天气”")
        continue

    # 追加对话
    messages.append({"role": "user", "content": user_input})
    try:
        response = requests.post(url, json={
            "model": "qwen:0.5b",
            "messages": messages,
            "stream": False
        })
        reply = response.json()["message"]["content"]
        print(f"Agent：{reply}\n")
        messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        print(f"出错：{e}")