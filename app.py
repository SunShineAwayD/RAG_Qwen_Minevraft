from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import config
from index_builder import get_or_build_index
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

config.setup_models()
index = get_or_build_index(
    data_path=config.JSON_DATA_PATH,
    index_save_path=config.INDEX_SAVE_PATH
)
query_engine = index.as_query_engine(similarity_top_k=3)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/query', methods=['POST'])
def query():
    data = request.json
    user_query = data.get('query', '')
    
    if not user_query:
        return jsonify({'error': '请输入问题'}), 400
    
    try:
        response = query_engine.query(user_query)
        
        sources = []
        for i, node in enumerate(response.source_nodes):
            sources.append({
                'question': node.metadata.get('question', 'N/A'),
                'source': node.metadata.get('source', 'N/A'),
                'score': float(node.score) if hasattr(node, 'score') else 0.0
            })
        
        return jsonify({
            'answer': str(response),
            'sources': sources
        })
    except Exception as e:
        return jsonify({'error': f'查询出错: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
