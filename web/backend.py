from flask import Flask, request, render_template, send_file, jsonify
import os
import uuid
from app.main import run_evaluation

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
RESULT_FOLDER = './results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('files')
    file_paths = []
    for file in files:
        save_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}_{file.filename}")
        file.save(save_path)
        file_paths.append(save_path)
    # 运行评测
    result_excel = os.path.join(RESULT_FOLDER, f"result_{uuid.uuid4()}.xlsx")
    accuracy = run_evaluation(file_paths, result_excel)
    return jsonify({
        "accuracy": accuracy,
        "excel_url": f"/download/{os.path.basename(result_excel)}"
    })

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(RESULT_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000) 