# tests/unit/test_utils.py
import pytest
import json
import uuid
from unittest.mock import patch, Mock, MagicMock

# Import the functions we want to test
from app.core.utils import clean_text, is_json_serializable, fetch_full_article


class TestCleanText:
    """Test the clean_text function"""
    
    def test_clean_text_basic_cleaning(self):
        """Test basic text cleaning functionality"""
        # Arrange
        dirty_text = "This  has   too    many     spaces"
        expected = "This has too many spaces"
        
        # Act
        result = clean_text(dirty_text)
        
        # Assert
        assert result == expected
    
    def test_clean_text_removes_control_characters(self):
        """Test that control characters are removed and whitespace collapsed"""
        # Arrange - using actual control characters
        dirty_text = "Hello\x00\x1f\x7fWorld"
        expected = "Hello World"  # Control chars become spaces, then collapsed
        
        # Act
        result = clean_text(dirty_text)
        
        # Assert
        assert result == expected
    
    def test_clean_text_handles_backslashes_and_quotes(self):
        """Test backslash and quote replacement"""
        # Arrange
        dirty_text = 'This has \\ backslashes and "quotes"'
        expected = "This has backslashes and 'quotes'"  # Spaces collapsed
        
        # Act
        result = clean_text(dirty_text)
        
        # Assert
        assert result == expected
    
    def test_clean_text_handles_non_string_input(self):
        """Test that non-string input returns empty string"""
        # Test various non-string inputs
        assert clean_text(None) == ""
        assert clean_text(123) == ""
        assert clean_text([]) == ""
        assert clean_text({}) == ""
    
    def test_clean_text_empty_string(self):
        """Test empty string input"""
        assert clean_text("") == ""
        assert clean_text("   ") == ""  # Only whitespace


class TestIsJsonSerializable:
    """Test the is_json_serializable function"""
    
    def test_json_serializable_valid_article(self):
        """Test with a valid, serializable article"""
        # Arrange
        valid_article = {
            "id": "123",
            "title": "Test Article",
            "content": "Some content",
            "url": "https://example.com"
        }
        
        # Act
        result = is_json_serializable(valid_article)
        
        # Assert
        assert result is True
    
    def test_json_serializable_with_unicode(self):
        """Test with unicode characters"""
        # Arrange
        unicode_article = {
            "title": "Test with émojis 🚀 and ñoño",
            "content": "Content with 中文 characters"
        }
        
        # Act
        result = is_json_serializable(unicode_article)
        
        # Assert
        assert result is True
    
    @patch('app.core.utils.logger')
    def test_json_serializable_invalid_data(self, mock_logger):
        """Test with non-serializable data"""
        # Arrange - functions can't be JSON serialized
        invalid_article = {
            "title": "Test",
            "invalid_field": lambda x: x  # Functions aren't JSON serializable
        }
        
        # Act
        result = is_json_serializable(invalid_article)
        
        # Assert
        assert result is False
        # Verify logger was called (showing it logged the error)
        mock_logger.error.assert_called()


class TestFetchFullArticle:
    """Test the fetch_full_article function"""
    
    @patch('app.core.utils.Article')
    def test_fetch_full_article_success(self, mock_article_class):
        """Test successful article fetching"""
        # Arrange
        mock_article = Mock()
        mock_article.text = "This is the full article content"
        mock_article_class.return_value = mock_article
        
        test_url = "https://example.com/article"
        
        # Act
        result = fetch_full_article(test_url)
        
        # Assert
        assert result == "This is the full article content"
        # Verify the Article class was used correctly
        mock_article_class.assert_called_once_with(test_url)
        mock_article.download.assert_called_once()
        mock_article.parse.assert_called_once()
    
    @patch('app.core.utils.Article')
    def test_fetch_full_article_failure(self, mock_article_class):
        """Test article fetching failure"""
        # Arrange
        mock_article_class.side_effect = Exception("Network error")
        test_url = "https://bad-url.com/article"
        
        # Act
        result = fetch_full_article(test_url)
        
        # Assert
        assert result.startswith("[Failed to fetch full article:")
        assert "Network error" in result
    
    @patch('app.core.utils.Article')
    @patch('app.core.utils.logger')
    def test_fetch_full_article_logs_debug_info(self, mock_logger, mock_article_class):
        """Test that debug information is logged"""
        # Arrange
        mock_article = Mock()
        mock_article.text = "Sample content"
        mock_article_class.return_value = mock_article
        
        test_url = "https://example.com/test"
        
        # Act
        result = fetch_full_article(test_url)
        
        # Assert
        assert result == "Sample content"
        # Verify debug logging was called
        mock_logger.debug.assert_called()