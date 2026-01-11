"""
记忆管理（Memory Management）实现

核心概念：Agent 保留并利用过去交互、观察和学习经验的能力。

使用前请确保已安装 common 包：
    cd learn_by_do
    pip install -e .
"""

from common import create_llm
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 使用 common 包中的 create_llm 创建语言模型
llm = create_llm(temperature=0)

# 构建对话历史（作为消息列表实现记忆）
conversation_history = [
    SystemMessage(content="你是一个有帮助的旅行代理。")
]

# 第一轮对话
user_message_1 = HumanMessage(content="我想预订航班。")
conversation_history.append(user_message_1)
response_1 = llm.invoke(conversation_history)
conversation_history.append(response_1)
print(f"用户：{user_message_1.content}")
print(f"助手：{response_1.content}\n")

# 第二轮对话
user_message_2 = HumanMessage(content="顺便说一下，我叫 Sam。")
conversation_history.append(user_message_2)
response_2 = llm.invoke(conversation_history)
conversation_history.append(response_2)
print(f"用户：{user_message_2.content}")
print(f"助手：{response_2.content}\n")

# 第三轮对话（测试记忆）
user_message_3 = HumanMessage(content="我的名字是什么？")
conversation_history.append(user_message_3)
response_3 = llm.invoke(conversation_history)
conversation_history.append(response_3)
print(f"用户：{user_message_3.content}")
print(f"助手：{response_3.content}")
