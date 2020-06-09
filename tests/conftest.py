import pytest
import sys, os

@pytest.fixture
def client():
    from app import app
    app.config['TESTING'] = True
    return app.test_client()