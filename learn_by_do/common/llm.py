"""
LLM 客户端封装

提供统一的 LLM 初始化函数，所有章节共享使用。
支持 LangChain 和 Google ADK 两种使用方式。
"""

import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


def create_llm(temperature: float = 0, model: str = None):
    """
    创建 LLM 实例，统一配置 API 密钥和基础 URL
    
    Args:
        temperature: 模型温度参数，默认 0
        model: 模型名称，如果不指定则从环境变量 OPENAI_MODEL 读取，默认为 gpt-3.5-turbo
        
    Returns:
        ChatOpenAI 实例
        
    Raises:
        ValueError: 如果未设置 OPENAI_API_KEY 环境变量
    """
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")
    
    # 如果未指定 model，则从环境变量读取，否则使用默认值
    if model is None:
        model = os.getenv("OPENAI_MODEL", "gpt-5_2-2025-12-11")
    
    if not api_key:
        raise ValueError("请设置 OPENAI_API_KEY 环境变量或在 .env 文件中配置")
    
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        openai_api_key=api_key,
        openai_api_base=base_url,
    )


def test_llm_connection(test_message: str = "你好，请回复'连接成功'", verbose: bool = True):
    """
    测试 LLM 连接和可用性
    
    Args:
        test_message: 测试消息内容
        verbose: 是否打印详细信息
        
    Returns:
        bool: 连接是否成功
        
    Raises:
        Exception: 如果连接失败，会抛出异常
    """
    try:
        if verbose:
            print("=" * 60)
            print("测试 LLM 连接...")
            print("=" * 60)
        
        # 创建 LLM 实例
        llm = create_llm(temperature=0)
        
        if verbose:
            print(f"✓ LLM 实例创建成功")
            print(f"  模型: {llm.model_name}")
            print(f"  基础 URL: {llm.openai_api_base or '默认 (OpenAI 官方)'}")
            print(f"\n发送测试消息: {test_message}")
        
        # 发送测试消息
        message = HumanMessage(content=test_message)
        response = llm.invoke([message])
        
        if verbose:
            print(f"\n✓ 收到响应:")
            print(f"  {response.content}")
            print("\n" + "=" * 60)
            print("✓ LLM 连接测试成功！")
            print("=" * 60)
        
        return True
        
    except ValueError as e:
        print(f"\n✗ 配置错误: {e}")
        print("请检查环境变量配置（OPENAI_API_KEY 等）")
        return False
        
    except Exception as e:
        print(f"\n✗ 连接失败: {e}")
        print("请检查:")
        print("  1. API 密钥是否正确")
        print("  2. 网络连接是否正常")
        print("  3. API 端点是否可访问")
        return False


def create_adk_model(model: str = None):
    """
    创建 Google ADK 的 LiteLLM 模型实例
    
    通过 LiteLLM 支持使用 OpenAI 兼容的 API，无需 Google API Key。
    
    Args:
        model: 模型名称，如果不指定则从环境变量 OPENAI_MODEL 读取
        
    Returns:
        LiteLlm 实例，可直接用于 Google ADK 的 LlmAgent
        
    Example:
        from common import create_adk_model
        from google.adk.agents import LlmAgent
        
        model = create_adk_model()
        agent = LlmAgent(name="my_agent", model=model, ...)
    """
    from google.adk.models.lite_llm import LiteLlm
    
    if model is None:
        model = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    base_url = os.getenv("OPENAI_BASE_URL")
    
    # LiteLLM 格式: "openai/model-name"
    if base_url:
        return LiteLlm(model=f"openai/{model}", api_base=base_url)
    else:
        return LiteLlm(model=f"openai/{model}")


if __name__ == "__main__":
    # 运行测试
    test_llm_connection()