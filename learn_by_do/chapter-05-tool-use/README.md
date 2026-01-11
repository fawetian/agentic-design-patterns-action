# 第5章：工具使用（Tool Use）

## 学习目标

- 理解工具使用模式的概念和应用场景
- 实现自定义工具
- 掌握工具调用机制

## 文件结构

```
chapter-05-tool-use/
├── README.md          # 本章说明文档
├── note.md            # 学习笔记
├── tool_use.py        # LangChain 工具使用示例
└── tool_use_adk.py    # Google ADK 工具使用示例
```

## 前置条件

1. 确保已按照 `learn_by_do/README.md` 中的说明完成环境配置
2. 确保已安装 `common` 包：`pip install -e .`（在 `learn_by_do` 目录下）
3. 配置环境变量（参考 `learn_by_do/env.example`）

## 运行示例

### LangChain 示例

```bash
conda activate ai
cd learn_by_do/chapter-05-tool-use
python tool_use.py
```

### Google ADK 示例

```bash
conda activate ai
cd learn_by_do/chapter-05-tool-use
python tool_use_adk.py
```

## 实现内容

### `tool_use.py` (LangChain 示例)

使用 `@tool` 装饰器定义工具，配合 `create_react_agent` 创建工具调用 Agent。

### `tool_use_adk.py` (Google ADK 示例)

- **FunctionTool**：将 Python 函数包装为 ADK 工具
- 示例工具：计算器、天气查询、信息搜索
- Agent 根据查询自动选择合适的工具

## 核心概念

**工具使用模式**：使 Agent 能连接外部 API、数据库、服务，甚至执行代码。

**关键组件**：
1. **工具定义**：使用装饰器或包装器定义工具
2. **工具选择**：LLM 根据查询选择合适的工具
3. **工具执行**：框架执行工具并返回结果
