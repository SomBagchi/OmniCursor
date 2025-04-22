import pytest
from unittest.mock import Mock, patch
import tkinter as tk
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ai_chat_assistant.__main__ import AIChatApp

@pytest.fixture
def mock_openai():
    with patch('src.ai_chat_assistant.__main__.OpenAI') as mock:
        mock.return_value.chat.completions.create.return_value.choices = [
            Mock(message=Mock(content="Test response"))
        ]
        yield mock

@pytest.fixture
def mock_env():
    with patch.dict('os.environ', {'OPENAI_API_KEY': 'test_key'}):
        yield

@pytest.fixture
def app(mock_openai, mock_env):
    """Create an app instance for testing"""
    root = tk.Tk()
    app = AIChatApp()
    yield app
    # Clean up
    if hasattr(app, 'root'):
        app.root.destroy()
    root.destroy()

def test_app_initialization(app):
    """Test that the app initializes correctly"""
    assert hasattr(app, 'root')
    assert hasattr(app, 'chat_history')
    assert hasattr(app, 'window_context')

def test_setup_openai(app, mock_env):
    """Test OpenAI setup with valid API key"""
    app.setup_openai()  # Should not raise an exception

def test_setup_openai_no_key(app):
    """Test OpenAI setup without API key"""
    # Clear any existing environment variables
    with patch.dict('os.environ', {}, clear=True):
        with pytest.raises(ValueError):
            app.setup_openai()

def test_get_window_context(app):
    """Test window context retrieval"""
    with patch('src.ai_chat_assistant.__main__.NSWorkspace') as mock_workspace:
        mock_app = Mock()
        mock_app.localizedName.return_value = "Test App"
        mock_workspace.sharedWorkspace.return_value.frontmostApplication.return_value = mock_app
        
        context = app.get_window_context()
        assert "Test App" in context

def test_capture_window_screenshot(app):
    """Test screenshot capture functionality"""
    with patch('Quartz.CGGetActiveDisplayList') as mock_get_displays, \
         patch('Quartz.CGDisplayCreateImage') as mock_create_image, \
         patch('PIL.Image.frombytes') as mock_image:
        
        # Mock display list
        mock_get_displays.return_value = 1
        mock_create_image.return_value = Mock(
            width=1920,
            height=1080,
            _data_provider=Mock()
        )
        mock_image.return_value = Mock(
            width=1920,
            height=1080,
            convert=Mock(return_value=Mock(
                save=Mock()
            ))
        )
        
        screenshots = app.capture_window_screenshot()
        assert screenshots is not None
        assert len(screenshots) > 0

def test_send_message(app, mock_openai):
    """Test message sending functionality"""
    # Create chat window
    app.create_chat_window()
    
    # Simulate sending a message
    app.input_field.insert(0, "Test message")
    app.send_message()
    
    # Check that message was added to history
    assert len(app.chat_history) > 0
    assert app.chat_history[-1]["role"] == "user"
    assert "Test message" in app.chat_history[-1]["content"]

def test_get_ai_response(app, mock_openai):
    """Test AI response generation"""
    # Create chat window first
    app.create_chat_window()
    
    # Mock the event handling
    with patch.object(app, '_handle_ai_response') as mock_handler:
        response = app.get_ai_response("Test message", [])
        
        # Test the behavior, not the content
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
        
        # Verify the handler was called
        mock_handler.assert_called_once()
        
        # Verify the response was stored
        assert app.root.getvar('ai_response') == response
