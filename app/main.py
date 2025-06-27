from csv_loader import load_csvs
from question_gen import generate_questions
from answer_eval import get_ai_answer_and_judge
from result_writer import write_results, print_accuracy

def run_evaluation(file_paths, output_excel):
    # file_paths: list of csv file paths
    docs = load_csvs(file_paths)
    results = []
    total = 0
    correct = 0

    for doc in docs:
        questions = generate_questions(doc['content'])
        for q in questions:
            ai_answer, is_correct = get_ai_answer_and_judge(q, doc['content'])
            results.append({
                "doc_name": doc['doc_name'],
                "question": q,
                "content": doc['content'],
                "ai_answer": ai_answer,
                "is_correct": is_correct
            })
            total += 1
            if is_correct == "正确":
                correct += 1

    write_results(results, output_excel)
    accuracy = correct / total if total else 0
    return accuracy

def main():
    # 1. 读取所有CSV
    docs = load_csvs()
    results = []
    total = 0
    correct = 0

    for doc in docs:
        questions = generate_questions(doc['content'])
        for q in questions:
            ai_answer, is_correct = get_ai_answer_and_judge(q, doc['content'])
            results.append({
                "doc_name": doc['doc_name'],
                "question": q,
                "content": doc['content'],
                "ai_answer": ai_answer,
                "is_correct": is_correct
            })
            total += 1
            if is_correct == "正确":
                correct += 1

    write_results(results)
    print_accuracy(correct, total)

if __name__ == "__main__":
    main() 