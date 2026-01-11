# 第4章：反思（Reflection）

## 学习目标

- 理解反思模式的概念和应用场景
- 实现自我评估和改进机制
- 掌握生成器-评审者模式

## 文件结构

```
chapter-04-reflection/
├── README.md           # 本章说明文档
├── note.md             # 学习笔记
├── reflection.py       # LangChain 反思示例
└── reflection_adk.py   # Google ADK 反思示例
```

## 前置条件

1. 确保已按照 `learn_by_do/README.md` 中的说明完成环境配置
2. 确保已安装 `common` 包：`pip install -e .`（在 `learn_by_do` 目录下）
3. 配置环境变量（参考 `learn_by_do/env.example`）

## 运行示例

### LangChain 示例

```bash
conda activate ai
cd learn_by_do/chapter-04-reflection
python reflection.py
```

### Google ADK 示例

```bash
conda activate ai
cd learn_by_do/chapter-04-reflection
python reflection_adk.py
```

## 实现内容

### `reflection.py` (LangChain 示例)

迭代反思循环：生成代码 → 评审 → 优化，直到满足质量标准。

### `reflection_adk.py` (Google ADK 示例)

- **SequentialAgent**：顺序执行生成器和评审者
- **生成器 Agent**：生成初始内容
- **评审者 Agent**：评估内容并提供反馈

## 核心概念

**反思模式**：Agent 评估自身工作并利用评估来提升性能。

**关键组件**：
1. **生成器**：产生初始输出
2. **评审者**：评估输出并提供反馈
3. **迭代优化**：基于反馈改进输出
