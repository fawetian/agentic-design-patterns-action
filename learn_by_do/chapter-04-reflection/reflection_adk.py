"""
反思（Reflection）实现 - Google ADK 版本

核心概念：使用 Google ADK 的 SequentialAgent 实现生成器-评审者模式。
一个 Agent 生成内容，另一个 Agent 评审并提供反馈。

使用前请确保已安装 common 包：
    cd learn_by_do
    pip install -e .
"""

import uuid
import asyncio
import nest_asyncio
from common import create_adk_model
from google.adk.agents import SequentialAgent, LlmAgent
from google.adk.runners import InMemoryRunner
from google.genai import types


# 获取模型配置
model = create_adk_model()

# --- 定义生成器 Agent ---
generator = LlmAgent(
    name="DraftWriter",
    model=model,
    description="生成关于给定主题的初始草稿内容。",
    instruction="撰写关于用户主题的简短、信息丰富的段落。",
    output_key="draft_text"  # 输出保存到此状态键
)

# --- 定义评审者 Agent ---
reviewer = LlmAgent(
    name="FactChecker",
    model=model,
    description="审查给定文本的事实准确性并提供结构化评审。",
    instruction="""
你是一个细致的事实核查员。
1. 阅读状态键 'draft_text' 中提供的文本。
2. 仔细验证所有声明的事实准确性。
3. 你的最终输出必须是包含两个部分的评审：
   - **状态**: "ACCURATE" 或 "INACCURATE"
   - **推理**: 提供对你的状态的清楚解释，如果发现任何问题则引用具体问题。

文本内容：{draft_text}
""",
    output_key="review_output"  # 结构化评审保存在这里
)

# --- SequentialAgent 确保生成器在评审者之前运行 ---
review_pipeline = SequentialAgent(
    name="WriteAndReview_Pipeline",
    sub_agents=[generator, reviewer],
    description="先生成内容，然后进行事实核查评审。"
)


# --- 执行逻辑 ---
async def run_reflection_pipeline(topic: str):
    """运行生成-评审管道。"""
    print(f"--- Google ADK 反思示例 ---")
    print(f"主题: {topic}\n")
    
    runner = InMemoryRunner(review_pipeline)
    
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
            parts=[types.Part(text=topic)]
        ),
    ):
        # 打印中间步骤
        if event.author == "DraftWriter" and event.content:
            if event.content.parts:
                text_parts = [part.text for part in event.content.parts if part.text]
                draft = "".join(text_parts)
                print("--- 生成的草稿 ---")
                print(draft)
                print()
        
        if event.is_final_response() and event.content:
            if event.content.parts:
                text_parts = [part.text for part in event.content.parts if part.text]
                final_result = "".join(text_parts)
            break
    
    print("--- 评审结果 ---")
    print(final_result)


async def main():
    """运行多个反思示例。"""
    await run_reflection_pipeline("量子计算的基本原理")
    print("\n" + "=" * 60 + "\n")
    await run_reflection_pipeline("人工智能在医疗领域的应用")


if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
