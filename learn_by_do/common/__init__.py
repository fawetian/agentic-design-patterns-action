"""
Common - 公共模块

存放所有章节共享的代码和配置。

使用方式（需要先安装）：
    cd learn_by_do
    pip install -e .

安装后即可直接导入：
    from common import create_llm, test_llm_connection
    from common import create_adk_model  # 用于 Google ADK
"""

from .llm import create_llm, test_llm_connection, create_adk_model

__all__ = ["create_llm", "test_llm_connection", "create_adk_model"]
