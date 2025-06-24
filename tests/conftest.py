
import pytest
import os
from unittest.mock import patch

@pytest.fixture(autouse=True, scope='session')
def setup_test_env():
    """Setup test environment for all tests"""
    test_env = {
        'SERPAPI_KEY': 'fake-serpapi-key-for-testing',
        'OPENAI_API_KEY': 'fake-openai-key-for-testing',
        'USE_STREAMLIT_SECRETS': 'false'
    }
    
    with patch.dict(os.environ, test_env):
        yield