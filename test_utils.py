import pytest
from unittest.mock import patch, MagicMock
from models import URL
import utils

def test_generate_short_url_with_custom_path():
    long_url = "https://example.com"
    custom_path = "custom_path"
    expected_url = URL(long_url=long_url, short_path=custom_path)
    
    with patch('utils.shortuuid.uuid') as mock_shortuuid:
        mock_shortuuid.return_value = custom_path
        
        # Call the generate_short_url function with custom_path
        result = utils.generate_short_url(long_url, custom_path)
        
        assert result == expected_url

def test_generate_short_url_without_custom_path():
    long_url = "https://example.com"
    expected_url = URL(long_url=long_url, short_path="generated_short_path")
    
    with patch('utils.shortuuid.uuid') as mock_shortuuid:
        mock_shortuuid.return_value = "generated_short_path"
        
        # Call the generate_short_url function without custom_path
        result = utils.generate_short_url(long_url)
        
        assert result == expected_url


