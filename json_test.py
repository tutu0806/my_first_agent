import json

# 1. 字典转JSON字符串 dumps
data = {
    "name": "agent学习",
    "age": 20,
    "skill": ["Python", "AI"]
}

# 转为json文本
json_str = json.dumps(data, ensure_ascii=False, indent=2)
print("字典转JSON：")
print(json_str)

# 2. JSON字符串转回字典 loads
back_data = json.loads(json_str)
print("\nJSON转回字典：")
print(back_data["name"])

# 3. 读写本地json配置文件
# 写入
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 读取
with open("config.json", "r", encoding="utf-8") as f:
    cfg = json.load(f)
print("\n读取配置文件：", cfg["skill"])