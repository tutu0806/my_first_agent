# 基于Ollama的本地AI智能助手 - 程序判断版（100%稳定）
import ollama
import re
from datetime import datetime
import operator
import requests

# ---------------------- 工具函数模块 ----------------------
def get_time():
    """获取系统当前时间并格式化"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def calculator(expression):
    """通用计算器：支持加减乘除运算"""
    try:
        return eval(expression, {"__builtins__": None}, {"operator": operator})
    except:
        return "计算错误"

def weather(city):
    """调用公开免费天气API，获取真实城市天气"""
    try:
        url = f"https://wttr.in/{city}?format=3"
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            return resp.text.strip()
        else:
            return f"{city} 天气查询失败"
    except:
        return f"{city} 网络异常，无法查询天气"

# ---------------------- 工具触发判断 ----------------------
def auto_trigger_tool(user_text):
    """程序自动判断用户问题，触发对应工具"""
    # 1. 时间判断
    if any(keyword in user_text for keyword in ["几点", "时间", "现在几点"]):
        return True, get_time()
    
    # 2. 天气判断（提取城市名）
    if any(keyword in user_text for keyword in ["天气", "气温", "温度"]):
        # 提取城市名（简单匹配，比如“北京天气”里的“北京”）
        match = re.search(r"(.{1,10})(天气|气温|温度)", user_text)
        if match:
            city = match.group(1)
            return True, weather(city)
    
    # 3. 计算判断（匹配算式）
    if re.search(r"[\d\+\-\*\/\(\)]+", user_text):
        # 提取算式
        expr = re.findall(r"[\d\+\-\*\/\(\)]+", user_text)[0]
        return True, calculator(expr)
    
    return False, None

class SimpleAgent:
    def __init__(self, model="qwen2.5:1.5b"):
        self.model = model
        self.history = []

    def chat(self, user_text):
        # 先让程序判断是否需要调用工具
        need_tool, tool_result = auto_trigger_tool(user_text)
        if need_tool:
            return f"成功调用 结果：{tool_result}"
        
        # 不需要工具，调用模型正常对话
        self.history.append({"role": "user", "content": user_text})
        res = ollama.chat(
            model=self.model,
            messages=[
                {"role": "system", "content": "你是一个友好的助手，正常回答用户问题。"},
                *self.history
            ]
        )
        ai_reply = res["message"]["content"]
        self.history.append({"role": "assistant", "content": ai_reply})
        return ai_reply

#程序入口运行
if __name__ == "__main__":
    print("本地AI智能助手已启动 | 输入 exit 退出")
    agent = SimpleAgent()
    while True:
        user_input = input("你：")
        if user_input.lower() == "exit":
            print("助手已退出")
            break
        print("AI：", agent.chat(user_input))