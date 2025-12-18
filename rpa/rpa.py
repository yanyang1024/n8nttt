import sys
import os
import csv
import json

def get_stock(product_name):
    """
    根据商品名称查询库存
    :param product_name: 商品名称关键词
    :return: 包含库存信息的字典
    """
    # 确定数据文件路径（相对于当前脚本位置）
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "inventory.csv")

    match_row = None
    
    if not os.path.exists(data_path):
        return {"error": f"Data file not found: {data_path}"}

    try:
        with open(data_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("Product", "")
                # 简单的模糊匹配，忽略大小写
                if product_name and product_name.lower() in name.lower():
                    match_row = row
                    break
        
        if match_row:
            stock = int(match_row.get("Stock") or 0)
            return {"found": True, "product": match_row.get("Product"), "stock": stock}
        else:
            return {"found": False, "product": product_name}
            
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # 获取命令行参数
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    
    # 执行查询
    result = get_stock(query)
    
    # 输出 JSON 结果
    print(json.dumps(result, ensure_ascii=False))

