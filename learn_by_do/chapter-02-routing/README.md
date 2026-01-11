# 第2章：路由（Routing）

## 学习目标

- 理解路由模式的概念和应用场景
- 实现基于条件的智能路由
- 掌握多路径分发策略

## 文件结构

```
chapter-02-routing/
├── README.md          # 本章说明文档
├── note.md            # 学习笔记
├── routing.py         # 路由模式示例代码（LangChain 版本）
├── routing_adk.py     # 路由模式示例代码（Google ADK 版本）
└── env.example        # 环境变量示例（参考父目录）
```

## 前置条件

1. 确保已按照 `learn_by_do/README.md` 中的说明完成环境配置
2. 确保已安装 `common` 包：`pip install -e .`（在 `learn_by_do` 目录下）
3. 配置环境变量（参考 `learn_by_do/env.example`）

## 运行示例

### LangChain 版本

```bash
# 激活 conda 环境
conda activate ai

# 进入本章目录
cd learn_by_do/chapter-02-routing

# 运行示例代码
python routing.py
```

### Google ADK 版本

```bash
# 安装依赖（如果尚未安装）
pip install google-adk litellm

# 使用与 routing.py 相同的环境变量配置（OPENAI_API_KEY, OPENAI_BASE_URL, OPENAI_MODEL）
# 通过 LiteLLM 支持 OpenAI 兼容的模型

# 运行 ADK 示例
python routing_adk.py
```

## 实现内容

### routing.py（LangChain 版本）

使用 LangChain 的 `RunnableBranch` 实现路由：
- **协调器路由链**：使用 LLM 分析用户意图
- **委托分支**：根据意图路由到不同的处理程序（预订、信息、澄清）
- 演示 `RunnableBranch` 和 `RunnablePassthrough` 的用法

### routing_adk.py（Google ADK 版本）

使用 Google Agent Development Kit 实现路由：
- **协调器 Agent**：分析请求并委托给子 Agent
- **专门子 Agent**：Booker（预订）和 Info（信息）
- **FunctionTool**：将 Python 函数包装为 Agent 工具
- 演示 ADK 的自动流委托机制

## 核心概念

**路由模式**：根据输入条件动态选择不同的处理路径，实现条件逻辑和决策分支。

**关键组件**：
1. **路由器（Router）**：分析输入并决定路由
2. **处理程序（Handlers）**：处理不同类别的请求
3. **分支逻辑（Branch Logic）**：根据路由决策分发请求

**路由方式**：
- **LLM路由**：使用语言模型分析意图，灵活但需要API调用
- **规则路由**：使用关键词或规则匹配，快速确定但灵活性较低
- **嵌入路由**：使用向量相似度（见第14章RAG）
- **ML模型路由**：使用专门训练的分类模型
