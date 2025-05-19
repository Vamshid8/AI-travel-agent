import pytest
from app import create_app
from models import db, User, TravelPlan
from datetime import datetime, timedelta

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_user(app):
    user = User(username='testuser', email='test@example.com')
    user.set_password('password123')
    db.session.add(user)
    db.session.commit()
    return user

def test_user_registration(client):
    response = client.post('/auth/register', json={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert User.query.filter_by(username='newuser').first() is not None

def test_user_login(client, test_user):
    response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_create_travel_plan(client, test_user):
    # First login to get token
    login_response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    token = login_response.json['access_token']
    
    # Create travel plan
    response = client.post('/api/travel-plans', 
        json={
            'destination': 'Paris',
            'start_date': (datetime.now() + timedelta(days=30)).isoformat(),
            'end_date': (datetime.now() + timedelta(days=37)).isoformat(),
            'budget': 2000,
            'currency': 'EUR',
            'preferences': 'Culture, Food, Museums'
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 201
    assert TravelPlan.query.filter_by(destination='Paris').first() is not None

def test_get_travel_plans(client, test_user):
    # First login to get token
    login_response = client.post('/auth/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    token = login_response.json['access_token']
    
    # Create a travel plan first
    client.post('/api/travel-plans', 
        json={
            'destination': 'Paris',
            'start_date': (datetime.now() + timedelta(days=30)).isoformat(),
            'end_date': (datetime.now() + timedelta(days=37)).isoformat(),
            'budget': 2000,
            'currency': 'EUR',
            'preferences': 'Culture, Food, Museums'
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    
    # Get travel plans
    response = client.get('/api/travel-plans',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert len(response.json) > 0 