import os
import pandas as pd
from .config import CSV_DIR

def load_csvs(file_paths=None):
    """
    支持三种用法：
    1. 不传参数，遍历CSV_DIR下所有csv文件
    2. 传入单个csv文件路径
    3. 传入csv文件路径列表
    返回每行的dict: {doc_name, title, content}
    """
    docs = []
    if file_paths is None:
        files = [os.path.join(CSV_DIR, fname) for fname in os.listdir(CSV_DIR) if fname.endswith('.csv')]
    elif isinstance(file_paths, str):
        files = [file_paths]
    else:
        files = file_paths
    for fpath in files:
        fname = os.path.basename(fpath)
        df = pd.read_csv(fpath)
        for _, row in df.iterrows():
            docs.append({
                "doc_name": fname,
                "title": row['标题'],
                "content": row['内容']
            })
    return docs 