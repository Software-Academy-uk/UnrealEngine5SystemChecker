import pytest
from main import check_system_specs, create_gui

# Test if system specs can be detected
def test_check_system_specs():
    specs = check_system_specs()
    
    # Check if CPU, RAM, Disk Space, and GPU are present in the specs
    assert 'CPU' in specs
    assert 'RAM' in specs
    assert 'Disk Space' in specs
    assert 'GPU' in specs

    # Ensure values are non-empty (basic check for functioning)
    assert specs['CPU'] != ''
    assert specs['RAM'] != ''
    assert specs['Disk Space'] != ''
    assert specs['GPU'] != ''

# Test if the GUI can launch (Tkinter window)
def test_create_gui():
    try:
        create_gui()  # Test if the GUI window opens
    except Exception as e:
        pytest.fail(f"GUI creation failed with error: {e}")
