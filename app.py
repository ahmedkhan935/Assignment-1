from flask import Flask, jsonify, request
import os

app = Flask(__name__)

items = [
    {"id": 1, "name": "Item 1", "description": "This is item 1"},
    {"id": 2, "name": "Item 2", "description": "This is item 2."}
]


@app.route('/', methods=['GET'])
def home():
    """Return a welcome message."""
    return jsonify({
        "message": "Welcome to the Simple Flask API",
        "version": "1.0.0",
        "endpoints": [
            "/api/items (GET, POST)",
            "/api/items/<id> (GET, PUT, DELETE)"
        ]
    })

@app.route('/api/items', methods=['GET'])
def get_items():
    """Return all items."""
    return jsonify({"items": items})
    
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
