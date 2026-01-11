# 第3章：并行化（Parallelization）

## 学习目标

- 理解并行化模式的概念和应用场景
- 实现并行任务处理
- 掌握结果聚合策略

## 文件结构

```
chapter-03-parallelization/
├── README.md               # 本章说明文档
├── note.md                 # 学习笔记
├── parallelization.py      # LangChain 并行化示例
└── parallelization_adk.py  # Google ADK 并行化示例
```

## 前置条件

1. 确保已按照 `learn_by_do/README.md` 中的说明完成环境配置
2. 确保已安装 `common` 包：`pip install -e .`（在 `learn_by_do` 目录下）
3. 配置环境变量（参考 `learn_by_do/env.example`）

## 运行示例

### LangChain 示例

```bash
conda activate ai
cd learn_by_do/chapter-03-parallelization
python parallelization.py
```

### Google ADK 示例

```bash
conda activate ai
cd learn_by_do/chapter-03-parallelization
python parallelization_adk.py
```

## 实现内容

### `parallelization.py` (LangChain 示例)

使用 `RunnableParallel` 并发执行多个独立的 LLM 调用，然后综合结果。

### `parallelization_adk.py` (Google ADK 示例)

- **ParallelAgent**：并发执行多个研究员 Agent
- **SequentialAgent**：协调并行研究和结果综合
- 多个研究员并行收集信息，综合 Agent 整合结果

## 核心概念

**并行化模式**：通过并发执行独立任务来提高效率，特别适用于涉及等待外部资源的任务。

**关键组件**：
1. **ParallelAgent**：并发执行多个子 Agent
2. **RunnableParallel**：LangChain 中并行执行多个可运行对象
3. **结果聚合**：收集并整合并行执行的结果
