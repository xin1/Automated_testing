import pandas as pd
from .config import OUTPUT_EXCEL

def write_results(results, output_excel=None):
    """
    将结果写入Excel，output_excel为None时用默认路径
    """
    df = pd.DataFrame(results)
    if output_excel is None:
        output_excel = OUTPUT_EXCEL
    df.to_excel(output_excel, index=False)

def print_accuracy(correct, total):
    """
    输出准确率
    """
    acc = correct / total if total else 0
    print(f"总问题数: {total}, 正确数: {correct}, 正确率: {acc:.2%}") 