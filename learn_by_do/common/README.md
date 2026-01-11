# Common - 公共模块

存放所有章节共享的代码和配置。

## 安装

首先需要安装 common 包为可编辑模式：

```bash
cd learn_by_do
pip install -e .
```

安装后即可在任意章节中直接导入，无需手动设置路径。

## 目录说明

- `llm.py` - LLM 客户端封装
- `__init__.py` - 包初始化文件，导出公共接口

## 使用方法

### LLM 客户端

所有章节统一使用 `create_llm()` 函数来初始化 LLM 客户端。

```python
# 简洁导入（推荐）
from common import create_llm

# 或者完整路径导入
from common.llm import create_llm

# 使用默认配置（从环境变量读取）
llm = create_llm(temperature=0)

# 或者指定模型
llm = create_llm(temperature=0, model="gpt-4o")
```

### Google ADK 模型

使用 `create_adk_model()` 函数创建 Google ADK 的 LiteLLM 模型实例：

```python
from common import create_adk_model
from google.adk.agents import LlmAgent

# 使用默认配置（从环境变量读取）
model = create_adk_model()

# 创建 ADK Agent
agent = LlmAgent(
    name="my_agent",
    model=model,
    instruction="你是一个有帮助的助手。"
)
```

通过 LiteLLM 支持使用 OpenAI 兼容的 API，无需 Google API Key。

### 测试 LLM 连接

可以使用 `test_llm_connection()` 函数测试 LLM 是否可用：

```python
from common import test_llm_connection

# 运行测试
test_llm_connection()

# 或者自定义测试消息
test_llm_connection(test_message="Hello, test connection", verbose=True)
```

也可以直接运行 `llm.py` 文件：

```bash
python -m common.llm
```

### 环境变量配置

需要在 `.env` 文件中配置以下变量：

```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1  # 可选，默认使用 OpenAI 官方端点
OPENAI_MODEL=gpt-3.5-turbo  # 可选，默认模型
```
