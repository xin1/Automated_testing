import pandas as pd
from .config import OUTPUT_EXCEL

def write_results(results):
    """
    将结果写入Excel
    """
    df = pd.DataFrame(results)
    df.to_excel(OUTPUT_EXCEL, index=False)

def print_accuracy(correct, total):
    """
    输出准确率
    """
    acc = correct / total if total else 0
    print(f"总问题数: {total}, 正确数: {correct}, 正确率: {acc:.2%}") 