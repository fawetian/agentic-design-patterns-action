"""
路由（Routing）实现 - Google ADK 版本

核心概念：使用 Google Agent Development Kit (ADK) 实现路由模式。
协调器 Agent 根据用户意图将请求委托给专门的子 Agent。

通过 LiteLLM 支持使用 OpenAI 兼容的模型，无需 Google API Key。

使用前请确保已安装 common 包：
    cd learn_by_do
    pip install -e .
"""

import os
import uuid
import asyncio
from common import create_adk_model
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool
from google.genai import types


# --- 定义工具函数 ---
def booking_handler(request: str) -> str:
    """
    处理航班和酒店的预订请求。
    参数：
        request: 用户的预订请求。
    返回：
        确认预订已处理的消息。
    """
    print("-------------------------- 调用预订处理程序 ----------------------------")
    return f"已模拟对 '{request}' 的预订操作。"


def info_handler(request: str) -> str:
    """
    处理一般信息请求。
    参数：
        request: 用户的问题。
    返回：
        表示信息请求已处理的消息。
    """
    print("-------------------------- 调用信息处理程序 ----------------------------")
    return f"对 '{request}' 的信息请求。结果：模拟信息检索。"


# --- 从函数创建工具 ---
booking_tool = FunctionTool(booking_handler)
info_tool = FunctionTool(info_handler)

# 使用 common 包中的 create_adk_model 获取模型配置
model = create_adk_model()

# 定义配备各自工具的专门子 Agent
booking_agent = LlmAgent(
    name="Booker",
    model=model,
    description="一个专门的 Agent，通过调用预订工具处理所有航班和酒店预订请求。",
    tools=[booking_tool]
)

info_agent = LlmAgent(
    name="Info",
    model=model,
    description="一个专门的 Agent，通过调用信息工具提供一般信息并回答用户问题。",
    tools=[info_tool]
)

# 定义具有明确委托指令的父 Agent（协调器）
coordinator = LlmAgent(
    name="Coordinator",
    model=model,
    instruction=(
        "你是主协调器。你唯一的任务是分析传入的用户请求"
        "并将它们委托给适当的专家 Agent。不要尝试直接回答用户。\n"
        "- 对于任何与预订航班或酒店相关的请求，委托给 'Booker' Agent。\n"
        "- 对于所有其他一般信息问题，委托给 'Info' Agent。"
    ),
    description="一个将用户请求路由到正确专家 Agent 的协调器。",
    # sub_agents 的存在默认启用 LLM 驱动的委托（自动流）。
    sub_agents=[booking_agent, info_agent]
)


# --- 执行逻辑 ---
async def run_coordinator(runner: InMemoryRunner, request: str):
    """使用给定请求运行协调器 Agent 并委托。"""
    print(f"\n--- 使用请求运行协调器: '{request}' ---")
    final_result = ""
    try:
        user_id = "user_123"
        session_id = str(uuid.uuid4())
        await runner.session_service.create_session(
            app_name=runner.app_name, user_id=user_id, session_id=session_id
        )
        
        for event in runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=types.Content(
                role='user',
                parts=[types.Part(text=request)]
            ),
        ):
            if event.is_final_response() and event.content:
                if hasattr(event.content, 'text') and event.content.text:
                    final_result = event.content.text
                elif event.content.parts:
                    text_parts = [part.text for part in event.content.parts if part.text]
                    final_result = "".join(text_parts)
                break
        
        print(f"协调器最终响应: {final_result}")
        return final_result
    except Exception as e:
        print(f"处理您的请求时出错: {e}")
        return f"处理您的请求时出错: {e}"


async def main():
    """运行 ADK 示例的主函数。"""
    print("--- Google ADK 路由示例（使用 LiteLLM + OpenAI 兼容模型）---")
    print(f"模型: {os.getenv('OPENAI_MODEL', 'gpt-4o')}")
    print(f"Base URL: {os.getenv('OPENAI_BASE_URL', '默认')}")
    
    runner = InMemoryRunner(coordinator)
    
    # 示例用法
    result_a = await run_coordinator(runner, "给我在巴黎预订一家酒店。")
    print(f"最终输出 A: {result_a}")
    
    result_b = await run_coordinator(runner, "世界上最高的山是什么？")
    print(f"最终输出 B: {result_b}")
    
    result_c = await run_coordinator(runner, "告诉我一个随机事实。")
    print(f"最终输出 C: {result_c}")
    
    result_d = await run_coordinator(runner, "查找下个月去东京的航班。")
    print(f"最终输出 D: {result_d}")


if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
