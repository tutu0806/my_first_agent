import json
import requests
from datetime import datetime

def calculate(expression):
    try:
        return str(eval(expression))
    except:
        return "计算失败，请输入正确的算式"

def get_time():
    now=datetime.now()
    return now.strftime("%Y年%m月%d日 %H:%M:%S")

def get_weather(city):
    weather_data={"东莞":"多云","揭阳":"下雨"}
    return weather_data.get(city,f"暂未收录该{city}的天气")

url="http://localhost:11434/api/chat"

messages=[{"role":"systerm","content":"你是一个友好，回答简洁的ai助手"}]
print("=== 🤖 半自动工具Agent已启动 ===")
print("你可以直接说：\n- 帮我算 1+1\n- 现在几点了\n- 东莞天气\n输入 exit 退出\n")
#判断是否退出对话
while True:
    user_input=input("你：")
    if user_input.lower() == "exit":
        print("agent：再见！")
        break


