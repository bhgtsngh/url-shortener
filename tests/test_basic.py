# tests/test_main.py
import pytest
from app.main import app as flask_app

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    return flask_app.test_client()

def test_shorten_url(client):
    response = client.post('/api/shorten', json={'url': 'https://example.com'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'short_code' in data
    assert data['short_url'].startswith('http://localhost:5000/')

def test_invalid_url(client):
    response = client.post('/api/shorten', json={'url': 'not-a-url'})
    assert response.status_code == 400

def test_redirect_and_stats(client):
    # shorten
    res = client.post('/api/shorten', json={'url': 'https://example.com'})
    short_code = res.get_json()['short_code']

    # redirect
    res = client.get(f'/{short_code}')
    assert res.status_code == 302

    # stats
    res = client.get(f'/api/stats/{short_code}')
    data = res.get_json()
    assert data['clicks'] == 1
    assert data['url'] == 'https://example.com'

def test_404_redirect(client):
    res = client.get('/nonexistent')
    assert res.status_code == 404

def test_404_stats(client):
    res = client.get('/api/stats/nonexistent')
    assert res.status_code == 404
