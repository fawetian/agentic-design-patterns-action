"""
多 Agent 协作（Multi-Agent Collaboration）实现 - Google ADK 版本

核心概念：展示 Google ADK 中的多种 Agent 协作模式：
- 层次化 Agent（父子关系）
- SequentialAgent（顺序执行）
- ParallelAgent（并行执行）
- Agent 作为工具

使用前请确保已安装 common 包：
    cd learn_by_do
    pip install -e .
"""

import uuid
import asyncio
import nest_asyncio
from typing import AsyncGenerator
from common import create_adk_model
from google.adk.agents import LlmAgent, BaseAgent, SequentialAgent, ParallelAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.runners import InMemoryRunner
from google.adk.tools import FunctionTool, agent_tool
from google.genai import types


# 获取模型配置
model = create_adk_model()


# ============================================================
# 示例 1：层次化 Agent（父子关系）
# ============================================================

class TaskExecutor(BaseAgent):
    """具有自定义非 LLM 行为的专门 Agent。"""
    name: str = "TaskExecutor"
    description: str = "执行预定义的任务。"
    
    async def _run_async_impl(self, context: InvocationContext) -> AsyncGenerator[Event, None]:
        """任务的自定义实现逻辑。"""
        yield Event(author=self.name, content=types.Content(
            parts=[types.Part(text="任务成功完成。")]
        ))


def create_hierarchical_agents():
    """创建层次化 Agent 结构示例。"""
    greeter = LlmAgent(
        name="Greeter",
        model=model,
        instruction="你是一个友好的欢迎者。用热情的方式问候用户。"
    )
    
    task_doer = TaskExecutor()
    
    coordinator = LlmAgent(
        name="Coordinator",
        model=model,
        description="可以欢迎用户并执行任务的协调者。",
        instruction="当被要求欢迎时，委托给 Greeter。当被要求执行任务时，委托给 TaskExecutor。",
        sub_agents=[greeter, task_doer]
    )
    
    # 验证父子关系
    assert greeter.parent_agent == coordinator
    assert task_doer.parent_agent == coordinator
    
    print("✓ 层次化 Agent 结构创建成功")
    return coordinator


# ============================================================
# 示例 2：SequentialAgent（顺序执行）
# ============================================================

def create_sequential_pipeline():
    """创建顺序执行管道示例。"""
    # Step 1: 数据获取
    step1 = LlmAgent(
        name="Step1_Fetch",
        model=model,
        instruction="你是数据收集专家。根据用户的主题，提供一些基本事实和数据。",
        output_key="data"
    )
    
    # Step 2: 数据处理
    step2 = LlmAgent(
        name="Step2_Process",
        model=model,
        instruction="""分析在 state['data'] 中找到的信息并提供摘要。
        
数据内容：{data}

请提供一个结构化的分析摘要。"""
    )
    
    pipeline = SequentialAgent(
        name="DataPipeline",
        sub_agents=[step1, step2],
        description="顺序执行数据获取和处理。"
    )
    
    print("✓ 顺序执行管道创建成功")
    return pipeline


# ============================================================
# 示例 3：ParallelAgent（并行执行）
# ============================================================

def create_parallel_gatherer():
    """创建并行数据收集器示例。"""
    weather_fetcher = LlmAgent(
        name="WeatherFetcher",
        model=model,
        instruction="你是天气专家。根据用户提到的位置，提供天气信息（可以是虚构的）。",
        output_key="weather_data"
    )
    
    news_fetcher = LlmAgent(
        name="NewsFetcher",
        model=model,
        instruction="你是新闻专家。根据用户提到的主题，提供相关新闻摘要（可以是虚构的）。",
        output_key="news_data"
    )
    
    data_gatherer = ParallelAgent(
        name="DataGatherer",
        sub_agents=[weather_fetcher, news_fetcher],
        description="并行获取天气和新闻数据。"
    )
    
    print("✓ 并行数据收集器创建成功")
    return data_gatherer


# ============================================================
# 示例 4：Agent 作为工具
# ============================================================

def generate_image(prompt: str) -> dict:
    """
    基于文本提示词生成图像（模拟）。
    
    参数：
        prompt：要生成的图像的详细描述。
        
    返回：
        包含状态和生成的图像信息的字典。
    """
    print(f"--- 🎨 工具调用：生成图像，提示词：'{prompt}' ---")
    return {
        "status": "success",
        "message": f"已根据提示词 '{prompt}' 生成图像",
        "image_url": "https://example.com/generated_image.png"
    }


def create_agent_as_tool():
    """创建 Agent 作为工具的示例。"""
    image_tool = FunctionTool(generate_image)
    
    # 图像生成 Agent
    image_generator = LlmAgent(
        name="ImageGen",
        model=model,
        instruction="""你是一个图像生成专家。
当收到请求时，使用 generate_image 工具创建图像。
描述你生成的图像。""",
        tools=[image_tool]
    )
    
    # 艺术家 Agent（调用图像生成器）
    artist_agent = LlmAgent(
        name="Artist",
        model=model,
        instruction="""你是一位创意艺术家。
1. 首先，根据用户的请求发明一个创意图像提示词
2. 然后委托给 ImageGen 来生成图像
3. 描述最终的艺术作品""",
        sub_agents=[image_generator]
    )
    
    print("✓ Agent 作为工具示例创建成功")
    return artist_agent


# ============================================================
# 运行示例
# ============================================================

async def run_agent(agent, query: str, name: str):
    """运行指定的 Agent。"""
    print(f"\n{'=' * 60}")
    print(f"运行 {name}")
    print(f"查询: {query}")
    print('=' * 60)
    
    runner = InMemoryRunner(agent)
    
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
    
    print(f"\n--- 结果 ---")
    print(final_result)


async def main():
    """运行所有多 Agent 协作示例。"""
    print("--- Google ADK 多 Agent 协作示例 ---\n")
    
    # 创建所有 Agent
    hierarchical = create_hierarchical_agents()
    sequential = create_sequential_pipeline()
    parallel = create_parallel_gatherer()
    agent_tool = create_agent_as_tool()
    
    print("\n" + "=" * 60)
    print("开始运行示例...")
    
    # 运行顺序管道示例
    await run_agent(
        sequential,
        "人工智能的发展历史",
        "顺序执行管道 (SequentialAgent)"
    )
    
    # 运行并行收集器示例
    await run_agent(
        parallel,
        "北京的天气和科技新闻",
        "并行数据收集器 (ParallelAgent)"
    )


if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
