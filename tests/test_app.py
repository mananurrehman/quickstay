import pytest
from app import create_app


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    yield app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


def test_app_creates_successfully(app):
    """Flask app factory returns an app."""
    assert app is not None


def test_app_is_in_testing_mode(app):
    """App is configured with TESTING=True."""
    assert app.config['TESTING'] is True


def test_home_page_responds(client):
    """Home route returns 200 or 302."""
    response = client.get('/')
    assert response.status_code in [200, 302]


def test_login_page_responds(client):
    """Login route is reachable."""
    response = client.get('/auth/login')
    assert response.status_code in [200, 302]


def test_register_page_responds(client):
    """Register route is reachable."""
    response = client.get('/auth/register')
    assert response.status_code in [200, 302]


def test_404_returns_correct_status(client):
    """Non-existent route returns 404."""
    response = client.get('/this-page-does-not-exist')
    assert response.status_code == 404