"""
路由（Routing）实现

核心概念：根据输入条件动态选择不同的处理路径，实现条件逻辑和决策分支。

使用前请确保已安装 common 包：
    cd learn_by_do
    pip install -e .
"""

from common import create_llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableBranch

# --- 定义模拟子 Agent 处理程序（相当于 ADK 的 sub_agents）---
def booking_handler(request: str) -> str:
    """模拟预订 Agent 处理请求。"""
    print("\n--- 委托给预订处理程序 ---")
    return f"预订处理程序处理了请求：'{request}'。结果：模拟预订操作。"

def info_handler(request: str) -> str:
    """模拟信息 Agent 处理请求。"""
    print("\n--- 委托给信息处理程序 ---")
    return f"信息处理程序处理了请求：'{request}'。结果：模拟信息检索。"

def unclear_handler(request: str) -> str:
    """处理无法委托的请求。"""
    print("\n--- 处理不清楚的请求 ---")
    return f"协调器无法委托请求：'{request}'。请澄清。"

# --- 定义协调器路由链（相当于 ADK 协调器的指令）---
# 此链决定应委托给哪个处理程序。
coordinator_router_prompt = ChatPromptTemplate.from_messages([
    ("system", """分析用户的请求并确定哪个专家处理程序应处理它。
     - 如果请求与预订航班或酒店相关，
        输出 'booker'。
     - 对于所有其他一般信息问题，输出 'info'。
     - 如果请求不清楚或不适合任一类别，
        输出 'unclear'。
     只输出一个词：'booker'、'info' 或 'unclear'。"""),
    ("user", "{request}")
])

llm = create_llm(temperature=0)
coordinator_router_chain = coordinator_router_prompt | llm | StrOutputParser()

# --- 定义委托逻辑（相当于 ADK 的基于 sub_agents 的自动流）---
# 使用 RunnableBranch 根据路由链的输出进行路由。
# 为 RunnableBranch 定义分支
branches = {
    "booker": RunnablePassthrough.assign(output=lambda x: booking_handler(x['request']['request'])),
    "info": RunnablePassthrough.assign(output=lambda x: info_handler(x['request']['request'])),
    "unclear": RunnablePassthrough.assign(output=lambda x: unclear_handler(x['request']['request'])),
}

# 创建 RunnableBranch。它接受路由链的输出
# 并将原始输入（'request'）路由到相应的处理程序。
delegation_branch = RunnableBranch(
    (lambda x: x['decision'].strip() == 'booker', branches["booker"]),
    (lambda x: x['decision'].strip() == 'info', branches["info"]),
    branches["unclear"] # 'unclear' 或任何其他输出的默认分支
)

# 将路由链和委托分支组合成单个可运行对象
# 路由链的输出（'decision'）与原始输入（'request'）一起传递
# 到 delegation_branch。
coordinator_agent = {
    "decision": coordinator_router_chain,
    "request": RunnablePassthrough()
} | delegation_branch | (lambda x: x['output']) # 提取最终输出

# --- 示例用法 ---
request_a = "给我预订去伦敦的航班。"
result_a = coordinator_agent.invoke({"request": request_a})
print(f"最终结果 A: {result_a}")

request_b = "意大利的首都是什么？"
result_b = coordinator_agent.invoke({"request": request_b})
print(f"最终结果 B: {result_b}")

request_c = "告诉我关于量子物理学的事。"
result_c = coordinator_agent.invoke({"request": request_c})
print(f"最终结果 C: {result_c}")
