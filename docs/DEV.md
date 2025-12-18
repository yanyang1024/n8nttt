# 💻 二次开发指南

本指南将帮助你定制和扩展 Demo 的功能。

## 1. 修改库存数据源

目前数据源是 `data/inventory.csv`。如果你想对接真正的 Excel 文件：

1.  安装依赖：`pip install pandas openpyxl`
2.  修改 `rpa/rpa.py`：
    ```python
    import pandas as pd
    # ...
    def get_stock(product_name):
        # ...
        df = pd.read_excel(excel_path)
        # 使用 pandas 进行查询逻辑
    ```

## 2. 对接 Dify (升级大脑)

如果你已经在其他机器或 Docker 环境部署了 Dify，可以接管 Prompt 管理：

1.  在 Dify 创建一个 **文本生成应用**。
2.  在 n8n 中修改 **HTTP Request** 节点：
    *   **URL**: `http://<dify-ip>/v1/completion-messages`
    *   **Header**: `Authorization: Bearer <YOUR-DIFY-API-KEY>`
    *   **Body**:
        ```json
        {
          "inputs": {
            "query": "{{ $('Read Query File').item.json.data }}",
            "stock_data": "{{ $json.stdout }}"
          },
          "response_mode": "blocking",
          "user": "n8n-user"
        }
        ```
    *   **注意**: 你需要在 Dify 的 Prompt 中预设好 `query` 和 `stock_data` 这两个变量。

## 3. 对接飞书/钉钉 (升级手脚)

将 **Local File Trigger** 替换为 **Webhook** 节点：

1.  **Webhook Node**: 设置为 POST，路径如 `/webhook/stock-query`。
2.  **飞书机器人**: 配置回调地址为 n8n 的 Webhook 地址（需公网可访问，或使用内网穿透工具如 cpolar/ngrok）。
3.  **后续节点**: 保持不变，最后将 **Write File** 节点替换为 **HTTP Request**，调用飞书 API 发送消息回群组。

## 4. 调试 RPA 脚本

在开发 RPA 脚本时，建议单独在命令行测试：

```bash
cd n8n_demo
python rpa/rpa.py "MacBook"
```

确保输出的是合法的 JSON，不要有多余的 print 输出（如调试日志），否则 n8n 解析 JSON 会失败。如果需要调试信息，请输出到 stderr：

```python
import sys
print("Debug info...", file=sys.stderr)
```
