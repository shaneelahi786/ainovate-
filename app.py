from flask import Flask, send_from_directory, request, jsonify
import os
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Path to your JSON files folder
JSON_FOLDER = '/data/data/com.termux/files/home/ainovate/static/json'

# Route: Serve the index.html page
@app.route('/')
def index():
    return send_from_directory('/data/data/com.termux/files/home/ainovate/templates', 'index.html')

# Route: Get list of all categories (JSON file names without .json)
@app.route('/get_categories')
def get_categories():
    files = [f.replace('.json', '') for f in os.listdir(JSON_FOLDER) if f.endswith('.json')]
    return jsonify(files)

# Route: Get tools from a selected category
@app.route('/get_tools')
def get_tools():
    category = request.args.get('category')
    filepath = os.path.join(JSON_FOLDER, f"{category}.json")
    if not os.path.exists(filepath):
        return jsonify([])
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)

# Route: Search category suggestions based on input
@app.route('/search_suggestions')
def search_suggestions():
    query = request.args.get('query', '').strip().lower()
    suggestions = []

    for filename in os.listdir(JSON_FOLDER):
        if filename.endswith('.json'):
            name = filename.replace('.json', '').lower()
            if query in name:
                suggestions.append(filename.replace('.json', ''))

    suggestions = sorted(suggestions)[:10]  # Return top 10 matches
    return jsonify(suggestions)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
