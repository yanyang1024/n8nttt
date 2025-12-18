# 🚀 本地化智能库存查询助手 (n8n + Ollama + Python)

这是一个完全离线、无需 Docker、轻量级的智能库存查询 Demo。它演示了如何使用 **n8n** 作为编排中枢，调用 **Python** 脚本（模拟 RPA）获取数据，并结合 **Ollama**（本地 LLM）进行智能回复。

## 📂 目录结构

```
n8n_demo/
├── data/
│   └── inventory.csv      # 模拟的老旧系统数据库
├── docs/
│   ├── DESIGN.md          # 架构设计文档
│   └── DEV.md             # 二次开发指南
├── rpa/
│   └── rpa.py             # Python RPA 脚本，负责读取数据
├── workflow.json          # n8n 工作流导出文件 (可直接导入)
└── README.md              # 本说明文档
```

## 🛠️ 环境准备

1.  **Node.js**: 需安装 Node.js (v18+) 以运行 n8n。
2.  **Python**: 需安装 Python 3.x。
3.  **Ollama**: 需安装 Ollama 客户端并下载模型 (推荐 `qwen2.5:7b` 或 `llama3`)。

## 🚀 快速开始

### 1. 安装并启动 n8n
打开终端运行：
```bash
npm install n8n -g
n8n
```
启动后访问：`http://localhost:5678`

### 2. 启动 Ollama
打开新终端运行：
```bash
ollama serve
```
确保你已经下载了模型：`ollama pull qwen2.5:7b` (或其他模型)

### 3. 导入工作流
1.  在 n8n 界面，点击右上角菜单 -> **Import from File**。
2.  选择本项目中的 `workflow.json` 文件。
3.  **注意**：导入后请检查节点中的路径是否匹配你的实际路径（特别是 `D:/GR_C_FRAME/n8n_demo`），如果不同请手动修改。

### 4. 运行 Demo
1.  在 n8n 界面点击底部的 **Execute Workflow** (激活监听)。
2.  在 `n8n_demo` 文件夹下新建一个 `query.txt` 文件，内容填写：
    ```
    iPhone
    ```
3.  观察 n8n 界面，流程会自动运行：
    -   读取 `query.txt`
    -   调用 Python 脚本查询 `inventory.csv`
    -   发送数据给 Ollama 生成回复
    -   结果写入 `result.txt`
4.  打开 `result.txt` 查看 AI 的智能回复。

## 📝 常见问题

-   **路径错误**：n8n 里的路径必须是绝对路径。Windows 下注意斜杠方向，推荐使用 `/` 或 `\\`。
-   **中文乱码**：本 Demo 已在 Python 脚本中强制使用 UTF-8，确保你的编辑器也使用 UTF-8 编码。
-   **模型报错**：请确保 n8n HTTP Request 节点里的 `model` 参数与你 Ollama 实际下载的模型名称一致。
