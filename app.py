import json
import os
from flask import Flask, request, jsonify, render_template

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# データファイルのパスを定義
DATA_FILE = "study_data.json"

def load_data():
    """
    JSONファイルからデータを読み込みます。
    ファイルが存在しない場合は、初期データを返します。
    """
    if not os.path.exists(DATA_FILE):
        return {
            "study_log": [],
            "tasks": []
        }
    
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # ファイルの内容が不正な場合も初期データを返す
        return {
            "study_log": [],
            "tasks": []
        }

def save_data(data):
    """
    データをJSONファイルに保存します。
    """
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    """
    メインページ（index.html）をレンダリングします。
    """
    return render_template('index.html')

@app.route('/api/data', methods=['GET'])
def get_data():
    """
    全ての学習データとタスクデータを取得するためのAPIエンドポイント。
    """
    data = load_data()
    return jsonify(data)

@app.route('/api/update', methods=['POST'])
def update_data():
    """
    学習ログまたはタスクデータを更新するためのAPIエンドポイント。
    """
    data = load_data()
    req_data = request.json

    if 'study_log' in req_data:
        data['study_log'].append(req_data['study_log'])
    
    if 'tasks' in req_data:
        data['tasks'] = req_data['tasks']

    save_data(data)
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # 開発サーバーを起動
    app.run(debug=True)
