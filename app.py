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


@app.route('/api/items', methods=['POST'])

def create_item():

    """Create a new item."""

    data = request.get_json()

    

    if not data or not data.get('name'):

        return jsonify({"error": "Name is required"}), 400

    

    # Generate a new ID

    new_id = max(item["id"] for item in items) + 1 if items else 1

    

    new_item = {

        "id": new_id,

        "name": data.get('name'),

        "description": data.get('description', '')

    }

    

    items.append(new_item)

    return jsonify({"item": new_item}), 201


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
