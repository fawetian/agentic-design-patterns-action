"""
工具使用（Tool Use）实现 - Google ADK 版本

核心概念：使用 Google ADK 的工具机制，使 Agent 能够调用外部函数。
本示例展示如何定义和使用自定义工具。

使用前请确保已安装 common 包：
    cd learn_by_do
    pip install -e .
"""

import uuid
import asyncio
import nest_asyncio
from common import create_adk_model
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool
from google.genai import types


# 获取模型配置
model = create_adk_model()


# --- 定义工具函数 ---
def calculate(expression: str) -> str:
    """
    计算数学表达式并返回结果。
    
    参数：
        expression: 要计算的数学表达式，如 "2 + 3 * 4"
        
    返回：
        计算结果的字符串表示
    """
    print(f"--- 🛠️ 工具调用：calculate，表达式：'{expression}' ---")
    try:
        # 安全地计算表达式（仅限数学运算）
        allowed_chars = set("0123456789+-*/().** ")
        if not all(c in allowed_chars for c in expression):
            return f"错误：表达式包含不允许的字符"
        result = eval(expression)
        print(f"--- 工具结果：{result} ---")
        return f"计算结果：{expression} = {result}"
    except Exception as e:
        return f"计算错误：{e}"


def get_weather(city: str) -> str:
    """
    获取指定城市的天气信息（模拟）。
    
    参数：
        city: 城市名称
        
    返回：
        天气信息字符串
    """
    print(f"--- 🛠️ 工具调用：get_weather，城市：'{city}' ---")
    # 模拟天气数据
    weather_data = {
        "北京": "晴天，温度 25°C，湿度 40%",
        "上海": "多云，温度 28°C，湿度 65%",
        "深圳": "阵雨，温度 30°C，湿度 80%",
        "东京": "晴天，温度 22°C，湿度 55%",
        "伦敦": "阴天，温度 15°C，湿度 70%",
    }
    result = weather_data.get(city, f"抱歉，暂无 {city} 的天气数据")
    print(f"--- 工具结果：{result} ---")
    return result


def search_info(query: str) -> str:
    """
    搜索信息（模拟）。
    
    参数：
        query: 搜索查询
        
    返回：
        搜索结果字符串
    """
    print(f"--- 🛠️ 工具调用：search_info，查询：'{query}' ---")
    # 模拟搜索结果
    results = {
        "python": "Python 是一种解释型、高级通用编程语言，由 Guido van Rossum 创建。",
        "ai": "人工智能（AI）是计算机科学的一个分支，致力于创建能够执行通常需要人类智能的任务的系统。",
        "量子计算": "量子计算利用量子力学原理，如叠加和纠缠，来处理信息。",
    }
    
    for key, value in results.items():
        if key in query.lower():
            print(f"--- 工具结果：{value} ---")
            return value
    
    result = f"关于 '{query}' 的搜索结果：这是一个有趣的主题，值得深入研究。"
    print(f"--- 工具结果：{result} ---")
    return result


# --- 从函数创建工具 ---
calculate_tool = FunctionTool(calculate)
weather_tool = FunctionTool(get_weather)
search_tool = FunctionTool(search_info)

# --- 创建配备工具的 Agent ---
assistant_agent = LlmAgent(
    name="Assistant",
    model=model,
    instruction="""你是一个有帮助的助手，可以：
1. 使用 calculate 工具进行数学计算
2. 使用 get_weather 工具查询天气
3. 使用 search_info 工具搜索信息

根据用户的问题选择合适的工具来回答。""",
    description="一个配备多种工具的智能助手。",
    tools=[calculate_tool, weather_tool, search_tool]
)


# --- 执行逻辑 ---
async def run_agent_with_tools(query: str):
    """使用工具运行 Agent。"""
    print(f"\n--- 用户查询: '{query}' ---")
    
    runner = InMemoryRunner(assistant_agent)
    
    user_id = "user_123"
    session_id = str(uuid.uuid4())
    await runner.session_service.create_session(
        app_name=runner.app_name, user_id=user_id, session_id=session_id
    )
    
    final_result = ""
    for event in runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=types.Content(
            role='user',
            parts=[types.Part(text=query)]
        ),
    ):
        if event.is_final_response() and event.content:
            if event.content.parts:
                text_parts = [part.text for part in event.content.parts if part.text]
                final_result = "".join(text_parts)
            break
    
    print(f"--- Agent 响应 ---")
    print(final_result)
    return final_result


async def main():
    """运行多个工具使用示例。"""
    print("--- Google ADK 工具使用示例 ---\n")
    
    # 测试计算工具
    await run_agent_with_tools("请计算 (15 + 25) * 3 的结果")
    
    print("\n" + "=" * 60 + "\n")
    
    # 测试天气工具
    await run_agent_with_tools("北京今天的天气怎么样？")
    
    print("\n" + "=" * 60 + "\n")
    
    # 测试搜索工具
    await run_agent_with_tools("什么是人工智能？")


if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
