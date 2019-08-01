import pytest
from app import create_app

# Creates a fixture whose name is "app"
# and returns our flask server instance
@pytest.fixture
def app():
    return create_app(env='testing')
