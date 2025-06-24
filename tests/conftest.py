import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_config():
    """Mock config for all tests"""
    with patch('app.config.SERPAPI_KEY', 'fake-serpapi-key'), \
         patch('app.config.NUM_SOURCES', 10):
        yield