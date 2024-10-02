import pytest
from unittest.mock import patch, MagicMock

# Fixture to mock check_system_specs and reset for every test
@pytest.fixture
def mock_check_system_specs():
    with patch('system_check.check_system_specs') as mock:
        yield mock

# Fixture to mock detailed_button and detailed_widget (GUI components)
@pytest.fixture
def mock_gui_components():
    detailed_button = MagicMock()
    detailed_widget = MagicMock()
    return detailed_button, detailed_widget

# Test case for failing Unreal Engine 5 but passing Unreal Engine 4 recommended requirements
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_fail_ue5_pass_ue4(mock_check_system_specs, mock_gui_components):
    from main import test_unreal_engine
    mock_check_system_specs.side_effect = lambda: {
        'CPU': '4 cores', 
        'RAM': '4 GB', 
        'Disk Space': '50 GB free', 
        'GPU': 'No dedicated GPU'
    }
    
    detailed_button, detailed_widget = mock_gui_components
    output = test_unreal_engine(detailed_button, detailed_widget, is_testing=True)
    assert output == "Your system can run Unreal Engine 4, but not Unreal Engine 5."
