import pytest
from unittest.mock import patch

from main import install_python_pygame

# Fixture to mock check_system_specs and reset for every test
@pytest.fixture
def mock_check_system_specs():
    with patch('system_check.check_system_specs') as mock:
        yield mock  # Provide mock to the test

# Test case for fully passing Unreal Engine 5 recommended requirements
@pytest.mark.pass_ue5
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_pass_ue5(mock_check_system_specs):
    from main import test_unreal_engine
    # Use side_effect instead of return_value to ensure mock resets for each test
    mock_check_system_specs.side_effect = lambda: {
        'CPU': '4 cores', 
        'RAM': '8 GB', 
        'Disk Space': '100 GB free', 
        'GPU': 'Dedicated GPU'
    }
    output = test_unreal_engine(is_testing=True)
    assert output == "Yes, your system can run Unreal Engine 5!"

# Test case for passing Unreal Engine 5 minimum requirements
@pytest.mark.min_pass_ue5
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_min_pass_ue5(mock_check_system_specs):
    from main import test_unreal_engine
    # Mock specs that meet Unreal Engine 5 minimum requirements but not recommended
    mock_check_system_specs.side_effect = lambda: {
        'CPU': '2 cores', 
        'RAM': '4 GB', 
        'Disk Space': '100 GB free', 
        'GPU': 'No dedicated GPU'
    }
    output = test_unreal_engine(is_testing=True)
    assert output == "Your system meets the minimum requirements for Unreal Engine 5, but may not perform optimally."

# Test case for failing Unreal Engine 5 but passing Unreal Engine 4 recommended requirements
@pytest.mark.fail_ue5_pass_ue4
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_fail_ue5_pass_ue4(mock_check_system_specs):
    from main import test_unreal_engine
    # Mock specs that fail Unreal Engine 5 but pass Unreal Engine 4 recommended requirements
    mock_check_system_specs.side_effect = lambda: {
        'CPU': '4 cores', 
        'RAM': '4 GB', 
        'Disk Space': '50 GB free', 
        'GPU': 'No dedicated GPU'
    }
    output = test_unreal_engine(is_testing=True)
    assert output == "Your system can run Unreal Engine 4, but not Unreal Engine 5."

# Test case for failing Unreal Engine 5 but passing Unreal Engine 4 minimum requirements
@pytest.mark.fail_ue5_min_pass_ue4
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_fail_ue5_min_pass_ue4(mock_check_system_specs):
    from main import test_unreal_engine
    # Mock specs that fail Unreal Engine 5 but meet Unreal Engine 4 minimum requirements
    mock_check_system_specs.side_effect = lambda: {
        'CPU': '2 cores', 
        'RAM': '4 GB', 
        'Disk Space': '50 GB free', 
        'GPU': 'No dedicated GPU'
    }
    output = test_unreal_engine(is_testing=True)
    assert output == "Your system can run Unreal Engine 4, but not Unreal Engine 5."

# Test case for failing both Unreal Engine 5 and Unreal Engine 4
@pytest.mark.fail_ue5_fail_ue4
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_fail_ue5_fail_ue4(mock_check_system_specs):
    from main import test_unreal_engine
    # Mock specs that fail both Unreal Engine 5 and Unreal Engine 4
    mock_check_system_specs.side_effect = lambda: {
        'CPU': '1 core', 
        'RAM': '2 GB', 
        'Disk Space': '20 GB free', 
        'GPU': 'No dedicated GPU'
    }
    output = test_unreal_engine(is_testing=True)
    assert output == "No, your system cannot run Unreal Engine 4 or 5."

# Test auto-install of PyGame when Python is installed
@pytest.mark.python_pygame
@patch('main.check_python_installed', return_value=True)
@patch('main.subprocess.run')
@patch('main.messagebox.showinfo')
def test_install_pygame(mock_messagebox, mock_subprocess, mock_check_python_installed):
    install_python_pygame()
    
    # Check if PyGame was installed via subprocess
    mock_subprocess.assert_called_with([mock_subprocess.call_args[0][0], "-m", "pip", "install", "pygame"], check=True)
    mock_messagebox.assert_called_with("PyGame Installation", "PyGame has been successfully installed!")

# Test behavior when Python is not installed
@pytest.mark.no_python_pygame
@patch('main.check_python_installed', return_value=False)
@patch('main.webbrowser.open')
@patch('main.messagebox.showinfo')
def test_install_python_not_found(mock_messagebox, mock_webbrowser, mock_check_python_installed):
    install_python_pygame()

    # Check that the Python download page was opened
    mock_webbrowser.assert_called_once_with("https://www.python.org/downloads/")
    mock_messagebox.assert_called_once_with("Python Not Found", "Python is not installed on your system. Please install Python first.")