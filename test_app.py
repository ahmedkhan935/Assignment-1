import pytest
import json
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_route(client):
    """Test the home route returns correct welcome message."""
    response = client.get('/')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "Welcome to the Simple Flask API" in data["message"]
    assert "version" in data
    assert "endpoints" in data


def test_get_items(client):
    """Test getting all items."""
    response = client.get('/api/items')
    data = json.loads(response.data)
    assert response.status_code == 200
    assert "items" in data
    assert isinstance(data["items"], list)


def test_create_item(client):
    """Test creating a new item."""
    new_item = {"name": "Test Item", "description": "Created during testing"}
    response = client.post(
        '/api/items',
        data=json.dumps(new_item),
        content_type='application/json'
    )
    data = json.loads(response.data)
    assert response.status_code == 201
    assert "item" in data
    assert data["item"]["name"] == "Test Item"
    assert "id" in data["item"]


def test_get_item(client):
    """Test getting a specific item."""
    # First create an item
    new_item = {"name": "Get Test Item", "description": "For testing get"}
    post_response = client.post(
        '/api/items',
        data=json.dumps(new_item),
        content_type='application/json'
    )
    post_data = json.loads(post_response.data)
    item_id = post_data["item"]["id"]
    # Now try to get it
    get_response = client.get(f'/api/items/{item_id}')
    get_data = json.loads(get_response.data)
    assert get_response.status_code == 200
    assert "item" in get_data
    assert get_data["item"]["id"] == item_id
    assert get_data["item"]["name"] == "Get Test Item"


def test_update_item(client):
    """Test updating an item."""
    # First create an item
    new_item = {"name": "Update Test Item", "description": "Before update"}
    post_response = client.post(
        '/api/items',
        data=json.dumps(new_item),
        content_type='application/json'
    )
    post_data = json.loads(post_response.data)
    item_id = post_data["item"]["id"]
    # Now update it
    update_data = {"description": "After update"}
    put_response = client.put(
        f'/api/items/{item_id}',
        data=json.dumps(update_data),
        content_type='application/json'
    )
    put_data = json.loads(put_response.data)
    assert put_response.status_code == 200
    assert put_data["item"]["description"] == "After update"
    assert put_data["item"]["name"] == "Update Test Item"  # Name unchanged


def test_delete_item(client):
    """Test deleting an item."""
    # First create an item
    new_item = {"name": "Delete Test Item", "description": "To be deleted"}
    post_response = client.post(
        '/api/items',
        data=json.dumps(new_item),
        content_type='application/json'
    )
    post_data = json.loads(post_response.data)
    item_id = post_data["item"]["id"]
    # Now delete it
    delete_response = client.delete(f'/api/items/{item_id}')
    delete_data = json.loads(delete_response.data)
    assert delete_response.status_code == 200
    assert "message" in delete_data
    assert f"Item {item_id} deleted successfully" in delete_data["message"]
    # Verify it's gone
    get_response = client.get(f'/api/items/{item_id}')
    assert get_response.status_code == 404
