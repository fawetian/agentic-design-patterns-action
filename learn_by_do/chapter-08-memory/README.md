# 第8章：记忆管理（Memory Management）

## 学习目标

- 理解记忆管理模式的概念和应用场景
- 实现对话上下文保持
- 掌握 Session 和 State 管理

## 文件结构

```
chapter-08-memory/
├── README.md        # 本章说明文档
├── note.md          # 学习笔记
├── memory.py        # LangChain 记忆管理示例
└── memory_adk.py    # Google ADK 记忆管理示例
```

## 前置条件

1. 确保已按照 `learn_by_do/README.md` 中的说明完成环境配置
2. 确保已安装 `common` 包：`pip install -e .`（在 `learn_by_do` 目录下）
3. 配置环境变量（参考 `learn_by_do/env.example`）

## 运行示例

### LangChain 示例

```bash
conda activate ai
cd learn_by_do/chapter-08-memory
python memory.py
```

### Google ADK 示例

```bash
conda activate ai
cd learn_by_do/chapter-08-memory
python memory_adk.py
```

## 实现内容

### `memory.py` (LangChain 示例)

使用消息历史列表维护多轮对话上下文。

### `memory_adk.py` (Google ADK 示例)

展示 ADK 的记忆管理机制：
- **output_key**：自动保存 Agent 输出到状态
- **多轮对话**：维护对话历史和上下文
- **跨 Agent 状态共享**：在顺序管道中共享数据

## 核心概念

**记忆管理模式**：Agent 保留并利用过去交互、观察和学习经验的能力。

**ADK 核心概念**：
1. **Session**：独立的对话线程，记录消息和操作
2. **State**：存储在 Session 中的临时数据
3. **output_key**：自动将 Agent 输出保存到状态
4. **MemoryService**：长期知识的存储和检索（高级）

**状态前缀**：
- `user:` - 与用户 ID 关联，跨会话持久
- `app:` - 应用级别，所有用户共享
- `temp:` - 仅当前处理轮次有效
