import pytest
import uuid
from app import app, init_db

@pytest.fixture
def client():
    # Configure Flask for testing
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Ensure the database and default admin user exist before tests run
            init_db()
        yield client

# Test Case 1: Validate system health endpoint
def test_health_check(client):
    rv = client.get('/health')
    assert rv.status_code == 200
    assert rv.json['status'] == 'healthy'

# Test Case 2: Validate successful authentication with correct credentials
def test_valid_login(client):
    rv = client.post('/login', json={'username': 'admin', 'password': 'admin'})
    assert rv.status_code == 200
    assert rv.json['status'] == 'success'

# Test Case 3: Validate authentication rejection with incorrect credentials
def test_invalid_login(client):
    rv = client.post('/login', json={'username': 'fakeuser', 'password': 'wrongpassword'})
    assert rv.status_code == 401
    assert rv.json['status'] == 'error'
    assert 'Invalid credentials' in rv.json['message']

# Test Case 4: Validate creating a new client record
def test_add_new_client(client):
    # Generate a unique name using UUID to prevent UNIQUE constraint failures upon multiple test runs
    unique_name = f"Test Client {uuid.uuid4().hex[:8]}"
    rv = client.post('/api/clients', json={'name': unique_name})
    
    assert rv.status_code == 201
    assert 'saved' in rv.json['message']

# Test Case 5: Validate retrieving the list of all clients
def test_get_clients_list(client):
    rv = client.get('/api/clients')
    assert rv.status_code == 200
    assert 'clients' in rv.json
    assert isinstance(rv.json['clients'], list)
    