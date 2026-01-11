"""
多 Agent 协作（Multi-Agent Collaboration）实现

核心概念：多个独立或半独立的 Agent 协同工作以实现共同目标。

使用前请确保已安装 common 包：
    cd learn_by_do
    pip install -e .
"""

from common import create_llm
from crewai import Agent, Task, Crew, Process

# 使用 common 包中的 create_llm 创建语言模型
llm = create_llm(temperature=0.7)

# 定义具有特定角色和目标的 Agent
researcher = Agent(
    role='高级研究分析师',
    goal='查找并总结 AI 的最新趋势。',
    backstory="你是一位经验丰富的研究分析师，擅长识别关键趋势和综合信息。",
    verbose=True,
    allow_delegation=False,
)

writer = Agent(
    role='技术内容作家',
    goal='基于研究发现撰写清晰且引人入胜的博客文章。',
    backstory="你是一位熟练的作家，可以将复杂的技术主题转化为易于理解的内容。",
    verbose=True,
    allow_delegation=False,
)

# 为 Agent 定义任务
research_task = Task(
    description="研究 2024-2025 年人工智能中出现的前 3 个趋势。重点关注实际应用和潜在影响。",
    expected_output="前 3 个 AI 趋势的详细摘要，包括关键点和来源。",
    agent=researcher,
)

writing_task = Task(
    description="基于研究发现撰写一篇 500 字的博客文章。文章应该引人入胜且易于普通读者理解。",
    expected_output="一篇关于最新 AI 趋势的完整 500 字博客文章。",
    agent=writer,
    context=[research_task],
)

# 创建团队
blog_creation_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    llm=llm,
    verbose=True
)

# 执行团队
print("## 使用 Gemini 2.0 Flash 运行博客创建团队... ##")
try:
    result = blog_creation_crew.kickoff()
    print("\n------------------\n")
    print("## 团队最终输出 ##")
    print(result)
except Exception as e:
    print(f"\n发生意外错误：{e}")
