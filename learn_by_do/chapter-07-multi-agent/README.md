# 第7章：多 Agent 协作（Multi-Agent Collaboration）

## 学习目标

- 理解多 Agent 协作模式的概念和应用场景
- 实现 Agent 间的协调与通信
- 掌握层次化、顺序、并行等协作模式

## 文件结构

```
chapter-07-multi-agent/
├── README.md            # 本章说明文档
├── note.md              # 学习笔记
├── multi_agent.py       # CrewAI 多 Agent 示例
└── multi_agent_adk.py   # Google ADK 多 Agent 示例
```

## 前置条件

1. 确保已按照 `learn_by_do/README.md` 中的说明完成环境配置
2. 确保已安装 `common` 包：`pip install -e .`（在 `learn_by_do` 目录下）
3. 配置环境变量（参考 `learn_by_do/env.example`）

## 运行示例

### CrewAI 示例

```bash
conda activate ai
cd learn_by_do/chapter-07-multi-agent
python multi_agent.py
```

### Google ADK 示例

```bash
conda activate ai
cd learn_by_do/chapter-07-multi-agent
python multi_agent_adk.py
```

## 实现内容

### `multi_agent.py` (CrewAI 示例)

使用 CrewAI 创建研究员和作家 Agent，协作完成博客创作任务。

### `multi_agent_adk.py` (Google ADK 示例)

展示多种 Agent 协作模式：
- **层次化 Agent**：父子关系，协调器委托任务
- **SequentialAgent**：顺序执行数据获取和处理
- **ParallelAgent**：并行收集天气和新闻数据
- **Agent 作为工具**：一个 Agent 调用另一个 Agent

## 核心概念

**多 Agent 协作模式**：多个独立或半独立的 Agent 协同工作以实现共同目标。

**协作范式**：
1. **层次化**：父 Agent 协调子 Agent
2. **顺序执行**：Agent 按顺序执行，前一个的输出是下一个的输入
3. **并行执行**：多个 Agent 同时执行独立任务
4. **Agent 作为工具**：一个 Agent 将另一个 Agent 当作工具调用
