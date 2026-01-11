"""
模型上下文协议（Model Context Protocol - MCP）实现

核心概念：标准化接口使 LLM 能与外部资源交互。

使用前请确保已安装 common 包：
    cd learn_by_do
    pip install -e .
"""

# 注意：MCP 实现需要额外的依赖和配置
# 1. 安装 FastMCP: pip install fastmcp
# 2. 安装 ADK MCP 工具: pip install google-adk

# 以下是使用 FastMCP 创建简单 MCP 服务器的示例

from fastmcp import FastMCP

# 初始化 FastMCP 服务器。
mcp_server = FastMCP()

# 定义一个简单的工具函数。
# `@mcp_server.tool` 装饰器将此 Python 函数注册为 MCP 工具。
# 文档字符串成为 LLM 的工具描述。
@mcp_server.tool
def greet(name: str) -> str:
    """
    生成个性化的问候语。

    参数：
        name: 要问候的人的名字。

    返回：
        问候语字符串。
    """
    return f"Hello, {name}! Nice to meet you."

# 或者如果您想从脚本运行它：
if __name__ == "__main__":
    mcp_server.run(
        transport="http",
        host="127.0.0.1",
        port=8000
    )
