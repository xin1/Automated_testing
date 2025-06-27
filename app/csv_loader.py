import os
import pandas as pd
from .config import CSV_DIR

def load_csvs():
    """
    遍历CSV_DIR下所有csv文件，返回每行的dict: {doc_name, title, content}
    """
    docs = []
    for fname in os.listdir(CSV_DIR):
        if fname.endswith('.csv'):
            df = pd.read_csv(os.path.join(CSV_DIR, fname))
            for _, row in df.iterrows():
                docs.append({
                    "doc_name": fname,
                    "title": row['标题'],
                    "content": row['内容']
                })
    return docs 