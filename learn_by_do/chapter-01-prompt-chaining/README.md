# 第1章：提示链（Prompt Chaining）

## 学习目标

- 理解提示链的概念和应用场景
- 实现基本的提示链模式
- 掌握链式调用的最佳实践

## 实现内容

本目录包含提示词链模式的完整实现和测试代码。

### 文件结构

```
chapter-01-prompt-chaining/
├── README.md                  # 本文件
├── note.md                    # 学习笔记
├── prompt_chaining.py         # 提示词链实现代码
├── test_prompt_chaining.py    # 测试代码
└── env.example                # 环境变量配置示例
```

## 快速开始

### 前置条件

确保已按照 `learn_by_do/README.md` 中的说明配置好 conda 环境和依赖：

1. 创建并激活 conda 环境：`conda activate ai`
2. 安装项目（包含依赖和 common 包）：`cd .. && pip install -e .`

### 1. 配置环境变量

复制环境变量示例文件：

```bash
cp env.example .env
# 编辑 .env 文件，填入 OPENAI_API_KEY
```

或者直接设置环境变量：

```bash
export OPENAI_API_KEY=your_api_key_here
```

### 3. 运行示例代码

```bash
python prompt_chaining.py
```

### 4. 运行测试

```bash
# 运行所有测试（使用 Mock，不需要 API 密钥）
python test_prompt_chaining.py

# 或使用 pytest
pytest test_prompt_chaining.py -v
```

## 实现说明

### 核心类

1. **PromptChain** - 提示词链基础类
   - 提供创建提取链和转换链的基础方法
   - 支持自定义提示词模板

2. **SpecificationExtractor** - 技术规格提取器
   - 演示两步提示词链：提取信息 -> 转换为 JSON
   - 基于文档中的示例实现

3. **DocumentProcessor** - 文档处理器
   - 演示多步骤文档处理流程
   - 实现：总结 -> 提取趋势 -> 生成报告

### 使用示例

#### 示例1：技术规格提取

```python
from prompt_chaining import SpecificationExtractor

extractor = SpecificationExtractor()
input_text = "新款笔记本电脑型号配备 3.5 GHz 八核处理器、16GB 内存和 1TB NVMe 固态硬盘。"
result = extractor.extract(input_text)
print(result)
```

#### 示例2：文档处理链

```python
from prompt_chaining import DocumentProcessor

processor = DocumentProcessor()
document = "你的文档内容..."
results = processor.process(document)
print(results["summary"])
print(results["trends"])
print(results["report"])
```

## 测试说明

测试代码包含以下测试类：

1. **TestPromptChain** - 基础类测试
2. **TestSpecificationExtractor** - 规格提取器测试
3. **TestDocumentProcessor** - 文档处理器测试
4. **TestPromptChainIntegration** - 集成测试（需要 API 密钥）
5. **TestPromptChainScenarios** - 场景测试

大部分测试使用 Mock，不需要实际的 API 调用。只有集成测试需要真实的 API 密钥。

## 关键概念

### 提示词链的核心思想

1. **任务分解**：将复杂任务拆解为聚焦步骤序列
2. **链式处理**：每步使用前步输出作为输入
3. **可靠性提升**：通过模块化提高可控性和稳定性
4. **框架支持**：使用 LangChain 等框架管理多步序列

### 适用场景

- 任务对于单个提示词过于复杂
- 涉及多个不同的处理阶段
- 需要在步骤之间与外部工具交互
- 构建需要执行多步推理的 Agent 系统

## 参考资源

- [LangChain 文档](https://python.langchain.com/)
- [LangGraph 文档](https://langchain-ai.github.io/langgraph/)
- [提示工程指南](https://www.promptingguide.ai/techniques/chaining)
