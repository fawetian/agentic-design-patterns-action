"""
记忆管理（Memory Management）实现 - Google ADK 版本

核心概念：展示 Google ADK 中的 Session 和 State 管理：
- Session：独立的对话线程
- State：会话中的临时数据存储
- output_key：自动保存 Agent 输出到状态

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
from google.adk.sessions import InMemorySessionService
from google.genai import types


# 获取模型配置
model = create_adk_model()


# ============================================================
# 示例 1：使用 output_key 自动保存状态
# ============================================================

async def demo_output_key():
    """演示使用 output_key 自动保存 Agent 输出到状态。"""
    print("=" * 60)
    print("示例 1：使用 output_key 自动保存状态")
    print("=" * 60)
    
    # 定义带有 output_key 的 Agent
    greeting_agent = LlmAgent(
        name="Greeter",
        model=model,
        instruction="生成一个简短、友好的问候语。",
        output_key="last_greeting"  # 输出自动保存到此键
    )
    
    # 设置 Session
    app_name = "memory_demo"
    user_id = "user_123"
    session_id = str(uuid.uuid4())
    
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    print(f"初始状态: {session.state}")
    
    # 创建 Runner
    runner = InMemoryRunner(greeting_agent)
    runner.session_service = session_service
    
    # 运行 Agent
    user_message = types.Content(
        role='user',
        parts=[types.Part(text="你好")]
    )
    
    print("\n--- 运行 Agent ---")
    for event in runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=user_message
    ):
        if event.is_final_response() and event.content:
            if event.content.parts:
                text_parts = [part.text for part in event.content.parts if part.text]
                response = "".join(text_parts)
                print(f"Agent 响应: {response}")
    
    # 检查更新后的状态
    updated_session = await session_service.get_session(app_name, user_id, session_id)
    print(f"\nAgent 运行后的状态: {updated_session.state}")
    
    # 验证 output_key 是否生效
    if "last_greeting" in updated_session.state:
        print(f"✓ 成功：问候语已保存到 state['last_greeting']")


# ============================================================
# 示例 2：多轮对话中的记忆保持
# ============================================================

async def demo_conversation_memory():
    """演示多轮对话中的记忆保持。"""
    print("\n" + "=" * 60)
    print("示例 2：多轮对话中的记忆保持")
    print("=" * 60)
    
    # 创建对话 Agent
    conversation_agent = LlmAgent(
        name="ConversationAgent",
        model=model,
        instruction="""你是一个有帮助的助手。
记住用户告诉你的所有信息，并在后续对话中使用这些信息。
保持友好和一致的对话风格。"""
    )
    
    # 设置 Session
    app_name = "conversation_demo"
    user_id = "user_456"
    session_id = str(uuid.uuid4())
    
    runner = InMemoryRunner(conversation_agent)
    await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    # 多轮对话
    conversations = [
        "你好，我叫小明。",
        "我喜欢编程和阅读。",
        "你还记得我的名字吗？我有什么爱好？"
    ]
    
    for i, message in enumerate(conversations, 1):
        print(f"\n--- 第 {i} 轮对话 ---")
        print(f"用户: {message}")
        
        for event in runner.run(
            user_id=user_id,
            session_id=session_id,
            new_message=types.Content(
                role='user',
                parts=[types.Part(text=message)]
            )
        ):
            if event.is_final_response() and event.content:
                if event.content.parts:
                    text_parts = [part.text for part in event.content.parts if part.text]
                    response = "".join(text_parts)
                    print(f"Agent: {response}")


# ============================================================
# 示例 3：跨 Agent 的状态共享
# ============================================================

async def demo_state_sharing():
    """演示使用状态在 Agent 之间共享数据。"""
    print("\n" + "=" * 60)
    print("示例 3：跨 Agent 的状态共享")
    print("=" * 60)
    
    from google.adk.agents import SequentialAgent
    
    # Agent 1：收集用户偏好
    preference_collector = LlmAgent(
        name="PreferenceCollector",
        model=model,
        instruction="""根据用户的输入，提取他们的偏好。
输出格式：简洁地列出用户的偏好。""",
        output_key="user_preferences"
    )
    
    # Agent 2：基于偏好生成推荐
    recommender = LlmAgent(
        name="Recommender",
        model=model,
        instruction="""你是一个推荐专家。
根据 state 中的用户偏好生成个性化推荐。

用户偏好：{user_preferences}

请提供 3 个相关推荐。"""
    )
    
    # 创建顺序管道
    pipeline = SequentialAgent(
        name="RecommendationPipeline",
        sub_agents=[preference_collector, recommender],
        description="收集偏好并生成推荐。"
    )
    
    # 运行管道
    runner = InMemoryRunner(pipeline)
    
    user_id = "user_789"
    session_id = str(uuid.uuid4())
    await runner.session_service.create_session(
        app_name=runner.app_name,
        user_id=user_id,
        session_id=session_id
    )
    
    user_input = "我喜欢科幻电影、Python 编程和户外徒步。"
    print(f"用户输入: {user_input}")
    
    for event in runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=types.Content(
            role='user',
            parts=[types.Part(text=user_input)]
        )
    ):
        # 显示中间结果
        if event.author == "PreferenceCollector" and event.content:
            if event.content.parts:
                text_parts = [part.text for part in event.content.parts if part.text]
                if text_parts:
                    print(f"\n--- 提取的偏好 ---")
                    print("".join(text_parts))
        
        if event.is_final_response() and event.content:
            if event.content.parts:
                text_parts = [part.text for part in event.content.parts if part.text]
                if text_parts:
                    print(f"\n--- 个性化推荐 ---")
                    print("".join(text_parts))


async def main():
    """运行所有记忆管理示例。"""
    print("--- Google ADK 记忆管理示例 ---\n")
    
    await demo_output_key()
    await demo_conversation_memory()
    await demo_state_sharing()
    
    print("\n" + "=" * 60)
    print("所有示例运行完成！")
    print("=" * 60)


if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
