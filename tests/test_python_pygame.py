import pytest, sys
from unittest.mock import patch, MagicMock, call
from main import install_python_pygame
# Test auto-install of PyGame when Python is installed
@patch('main.check_python_installed', return_value=True)
@patch('main.subprocess.run')
@patch('main.messagebox.showinfo')
def test_install_pygame(mock_messagebox, mock_subprocess, mock_check_python_installed):
    install_python_pygame()

    # Update the test to match the correct subprocess call
    mock_subprocess.assert_called_with([sys.executable, "-m", "pip", "install", "pygame"], check=True)
    mock_messagebox.assert_called_with("PyGame Installation", "PyGame has been successfully installed!")

# Test behavior when Python is not installed
@patch('main.check_python_installed', return_value=False)
@patch('main.webbrowser.open')
@patch('main.messagebox.showinfo')
def test_install_python_not_found(mock_messagebox, mock_webbrowser, mock_check_python_installed):
    install_python_pygame()

    # Check that both the Python download link and the YouTube video link were opened
    expected_web_calls = [
        call('https://www.python.org/downloads/'),
        call('https://www.youtube.com/watch?v=cTwD_LC5F9A')
    ]
    
    assert mock_webbrowser.call_count == 2
    mock_webbrowser.assert_has_calls(expected_web_calls)

    # Ensure that both messagebox.showinfo calls were made
    expected_message_calls = [
        call("Python Not Found", "Python is not installed on your system. Please install Python first."),
        call("How to video", "Here is a short video on how to install Python.")
    ]

    assert mock_messagebox.call_count == 2
    mock_messagebox.assert_has_calls(expected_message_calls)