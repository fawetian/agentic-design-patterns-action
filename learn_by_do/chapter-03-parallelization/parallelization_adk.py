"""
并行化（Parallelization）实现 - Google ADK 版本

核心概念：使用 Google ADK 的 ParallelAgent 和 SequentialAgent 实现并发执行。
多个研究 Agent 并行收集信息，然后由综合 Agent 整合结果。

使用前请确保已安装 common 包：
    cd learn_by_do
    pip install -e .
"""

import uuid
import asyncio
import nest_asyncio
from common import create_adk_model
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.runners import InMemoryRunner
from google.genai import types


# 获取模型配置
model = create_adk_model()

# --- 1. 定义研究员子 Agent（并行运行）---
researcher_agent_1 = LlmAgent(
    name="RenewableEnergyResearcher",
    model=model,
    instruction="""你是一名专门研究能源的 AI 研究助理。
研究"可再生能源"的最新进展。
简洁地总结你的主要发现（1-2 句话）。*只*输出摘要。""",
    description="研究可再生能源。",
    output_key="renewable_energy_result"
)

researcher_agent_2 = LlmAgent(
    name="EVResearcher",
    model=model,
    instruction="""你是一名专门研究交通的 AI 研究助理。
研究"电动汽车技术"的最新发展。
简洁地总结你的主要发现（1-2 句话）。*只*输出摘要。""",
    description="研究电动汽车技术。",
    output_key="ev_technology_result"
)

researcher_agent_3 = LlmAgent(
    name="CarbonCaptureResearcher",
    model=model,
    instruction="""你是一名专门研究气候解决方案的 AI 研究助理。
研究"碳捕获方法"的当前状态。
简洁地总结你的主要发现（1-2 句话）。*只*输出摘要。""",
    description="研究碳捕获方法。",
    output_key="carbon_capture_result"
)

# --- 2. 创建 ParallelAgent（并发运行研究员）---
parallel_research_agent = ParallelAgent(
    name="ParallelResearchAgent",
    sub_agents=[researcher_agent_1, researcher_agent_2, researcher_agent_3],
    description="并行运行多个研究 Agent 以收集信息。"
)

# --- 3. 定义合并 Agent（在并行 Agent 之后运行）---
merger_agent = LlmAgent(
    name="SynthesisAgent",
    model=model,
    instruction="""你是一名负责将研究发现组合成结构化报告的 AI 助理。
综合以下研究摘要，清楚地将发现归属于其来源领域。

**输入摘要：**
* **可再生能源：** {renewable_energy_result}
* **电动汽车：** {ev_technology_result}
* **碳捕获：** {carbon_capture_result}

**输出格式：**
## 近期可持续技术进展摘要

### 可再生能源发现
[综合可再生能源输入摘要]

### 电动汽车发现
[综合电动汽车输入摘要]

### 碳捕获发现
[综合碳捕获输入摘要]

### 总体结论
[提供一个简短的结论性陈述]""",
    description="将并行 Agent 的研究发现组合成结构化报告。"
)

# --- 4. 创建 SequentialAgent（协调整体流程）---
sequential_pipeline_agent = SequentialAgent(
    name="ResearchAndSynthesisPipeline",
    sub_agents=[parallel_research_agent, merger_agent],
    description="协调并行研究并综合结果。"
)


# --- 执行逻辑 ---
async def run_parallel_research():
    """运行并行研究管道。"""
    print("--- Google ADK 并行化示例 ---")
    print("使用 ParallelAgent 并行执行多个研究任务，然后综合结果。\n")
    
    runner = InMemoryRunner(sequential_pipeline_agent)
    
    user_id = "user_123"
    session_id = str(uuid.uuid4())
    await runner.session_service.create_session(
        app_name=runner.app_name, user_id=user_id, session_id=session_id
    )
    
    request = "请研究可持续技术的最新进展。"
    print(f"用户请求: {request}\n")
    
    final_result = ""
    for event in runner.run(
        user_id=user_id,
        session_id=session_id,
        new_message=types.Content(
            role='user',
            parts=[types.Part(text=request)]
        ),
    ):
        if event.is_final_response() and event.content:
            if event.content.parts:
                text_parts = [part.text for part in event.content.parts if part.text]
                final_result = "".join(text_parts)
            break
    
    print("--- 最终综合报告 ---")
    print(final_result)


if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(run_parallel_research())
