import pytest
from unittest.mock import Mock, patch
import Quartz
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ai_chat_assistant.__main__ import AIChatApp

@pytest.fixture
def mock_quartz():
    with patch('Quartz.CGGetActiveDisplayList') as mock_get_displays, \
         patch('Quartz.CGDisplayCreateImage') as mock_create_image, \
         patch('Quartz.CGImageGetWidth') as mock_width, \
         patch('Quartz.CGImageGetHeight') as mock_height, \
         patch('Quartz.CGDataProviderCopyData') as mock_data:
        
        # Mock display list
        mock_get_displays.return_value = 2  # Two displays
        
        # Mock image data
        mock_width.return_value = 1920
        mock_height.return_value = 1080
        mock_data.return_value = b'\x00' * (1920 * 1080 * 4)  # RGBA data
        
        yield {
            'get_displays': mock_get_displays,
            'create_image': mock_create_image,
            'width': mock_width,
            'height': mock_height,
            'data': mock_data
        }

def test_multiple_displays(mock_quartz):
    """Test handling of multiple displays"""
    app = AIChatApp()
    
    # Mock the display list to return 2 displays
    mock_quartz['get_displays'].return_value = 2
    
    # Mock the display bounds
    with patch('Quartz.CGDisplayBounds') as mock_bounds:
        mock_bounds.return_value = Mock(origin=Mock(x=0, y=0), size=Mock(width=1920, height=1080))
        
        screenshots = app.capture_window_screenshot()
        assert screenshots is not None
        assert len(screenshots) == 2  # Should capture both displays
        assert all(s['width'] == 1024 for s in screenshots)  # After resizing
        assert all(s['height'] <= 1080 for s in screenshots)

def test_display_bounds(mock_quartz):
    """Test display bounds handling"""
    app = AIChatApp()
    
    # Mock CGDisplayBounds to return specific bounds
    with patch('Quartz.CGDisplayBounds') as mock_bounds:
        mock_bounds.return_value = Mock(origin=Mock(x=0, y=0), size=Mock(width=1920, height=1080))
        screenshots = app.capture_window_screenshot()
        
        assert screenshots is not None
        assert all(s['width'] == 1024 for s in screenshots)  # After resizing
        assert all(s['height'] <= 1080 for s in screenshots)

def test_image_conversion(mock_quartz):
    """Test image format conversion"""
    app = AIChatApp()
    screenshots = app.capture_window_screenshot()
    
    assert screenshots is not None
    for screenshot in screenshots:
        # Check that the image string is base64 encoded
        assert isinstance(screenshot['image'], str)
        assert len(screenshot['image']) > 0

def test_error_handling(mock_quartz):
    """Test error handling in screenshot capture"""
    app = AIChatApp()
    
    # Simulate an error in display creation
    mock_quartz['create_image'].return_value = None
    mock_quartz['get_displays'].return_value = 0  # No displays found
    
    # Mock all necessary functions to simulate a complete failure
    with patch('Quartz.CGDisplayBounds', side_effect=Exception("Display not found")), \
         patch('PIL.Image.frombytes', side_effect=Exception("Image creation failed")), \
         patch('base64.b64encode', side_effect=Exception("Encoding failed")):
        
        screenshots = app.capture_window_screenshot()
        assert screenshots is None  # Should return None on error
