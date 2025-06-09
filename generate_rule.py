import os
import re

# 读取文件
with open("./rules.yaml", "r") as file:
    rules = file.read()

# 创建文件夹
os.makedirs("./rules", exist_ok=True)

# 正则
regex = r"# ======= (.*?) ======= #"
result = re.split(regex, rules)

# 拆分 yaml文件
for i in range(1, len(result), 2):
    ruleName = result[i]
    ruleContent = result[i + 1]

    # 创建对应名称的文件
    filePath = f"./rules/{ruleName}.yaml"

    # 添加原始文件内容
    splitYAML = f"{result[0]}\n# ======= {ruleName} ======= #\n{ruleContent}"

    # 写入文件
    with open(filePath, "w") as file:
        file.write(splitYAML)
