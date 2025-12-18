# 🏗️ 系统架构设计文档

## 1. 设计理念

本项目基于 **"大脑-手脚-义肢"** 的仿生架构理念设计，旨在解决企业内部异构系统集成与智能化的痛点，同时遵循 **离线、轻量、低代码** 的约束。

### 核心组件

*   **大脑 (AI Kernel) - Ollama**: 
    *   **角色**: 认知中心。
    *   **职责**: 理解用户意图，处理非结构化数据，生成自然语言回复。
    *   **选型理由**: 单文件部署，无 Docker 依赖，提供标准 API，适合离线环境。

*   **手脚 (Orchestrator) - n8n**:
    *   **角色**: 调度与编排中心。
    *   **职责**: 监听外部事件（文件/Webhook），串联各个独立的组件，进行数据流转与转换。
    *   **选型理由**: 强大的可视化编排能力，npm 直接安装，生态丰富。

*   **义肢 (Legacy Access) - Python Script**:
    *   **角色**: 执行单元 (RPA)。
    *   **职责**: 深入“老旧系统”（模拟为 CSV/Excel），执行具体的数据读写操作。
    *   **选型理由**: 灵活性极高，能够处理各种非标接口、数据库或文件格式，弥补 n8n 标准节点的不足。

## 2. 数据流转图

```mermaid
graph LR
    User[用户] -->|创建 query.txt| Trigger(n8n: File Trigger)
    Trigger --> Reader(n8n: Read File)
    Reader -->|商品名| RPA[Python Script]
    RPA -->|读取| DB[(Inventory CSV)]
    DB -->|库存数据| RPA
    RPA -->|JSON: {found, stock}| n8n_Exec(n8n: Execute Command)
    n8n_Exec -->|Prompt + Context| AI(Ollama)
    AI -->|智能回复| Writer(n8n: Write File)
    Writer -->|生成 result.txt| User
```

## 3. 模块边界与接口

### 3.1 RPA 模块 (`rpa/rpa.py`)
*   **输入**: 命令行参数（商品名称关键词）。
*   **处理**: 读取 `data/inventory.csv`，进行模糊匹配。
*   **输出**: 标准输出 (stdout) 打印 JSON 字符串。
    *   成功: `{"found": true, "product": "iPhone 15", "stock": 5}`
    *   失败: `{"found": false, "product": "xxx"}`
    *   错误: `{"error": "error message"}`

### 3.2 AI 模块 (n8n HTTP Request -> Ollama)
*   **输入**: HTTP POST Body
    ```json
    {
      "model": "qwen2.5:7b",
      "prompt": "...",
      "stream": false
    }
    ```
*   **输出**: JSON，包含 `response` 字段（生成文本）。

## 4. 扩展性设计

*   **替换大脑**: 
    *   当前直接调用 Ollama。
    *   未来可升级为 **Dify**，只需将 n8n 中的 HTTP Request URL 改为 Dify 的 API Endpoint，并添加 Authorization Header。Dify 可提供更高级的 Prompt 编排和知识库检索 (RAG)。
*   **替换义肢**:
    *   当前为简单的 CSV 读取。
    *   未来可替换为 **Selenium/Playwright** 脚本去操作 Web 系统，或 **PyAutoGUI** 操作桌面软件。
*   **替换触发器**:
    *   当前为本地文件监听。
    *   未来可改为 **Webhook** 节点，对接飞书/钉钉机器人，实现即时通讯工具内的问答。
