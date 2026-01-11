"""
工具使用（Tool Use）实现

核心概念：使 Agent 能连接外部 API、数据库、服务，甚至执行代码。

使用前请确保已安装 common 包：
    cd learn_by_do
    pip install -e .
"""

from common import create_llm
from langchain_core.tools import tool as langchain_tool
from langchain.agents import create_agent

# 需要具有函数/工具调用能力的模型。
llm = create_llm(temperature=0)

# --- 定义工具 ---
@langchain_tool
def search_information(query: str) -> str:
    """
    提供有关给定主题的事实信息。使用此工具查找诸如"法国首都"或"伦敦的天气？"等短语的答案。
    """
    print(f"\n--- 🛠️ 工具调用：search_information，查询：'{query}' ---")
    
    # 使用预定义结果字典模拟搜索工具。
    simulated_results = {
        "weather in london": "伦敦目前多云，温度为 15°C。",
        "capital of france": "法国的首都是巴黎。",
        "population of earth": "地球的估计人口约为 80 亿人。",
        "tallest mountain": "珠穆朗玛峰是海拔最高的山峰。",
        "default": f"'{query}' 的模拟搜索结果：未找到特定信息，但该主题似乎很有趣。"
    }
    
    result = simulated_results.get(query.lower(), simulated_results["default"])
    print(f"--- 工具结果：{result} ---")
    return result

tools = [search_information]

# --- 创建 Agent ---
# create_agent 返回一个可以直接调用的图
agent = create_agent(model=llm, tools=tools)

# --- 运行 Agent ---
queries = [
    "法国的首都是什么？",
    "伦敦的天气怎么样？",
    "告诉我一些关于狗的事情。"
]

for query in queries:
    print(f"\n--- 🏃 使用查询运行 Agent：'{query}' ---")
    result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    
    # 获取最后一条消息的内容
    if result.get("messages"):
        last_message = result["messages"][-1]
        print("\n--- ✅ 最终 Agent 响应 ---")
        print(last_message.content)
