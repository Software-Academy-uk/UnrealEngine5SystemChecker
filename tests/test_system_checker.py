import pytest
from system_check import check_system_specs
from validation import validate_specs
import os

# Unreal Engine Requirements (Minimum and Recommended)
MINIMUM_REQUIREMENTS = {
    'CPU': 4,   # 4 cores
    'RAM': 8,   # 8 GB
    'Disk Space': 50,  # 50 GB free
    'GPU': True  # Dedicated GPU
}

RECOMMENDED_REQUIREMENTS = {
    'CPU': 6,   # 6 cores or more
    'RAM': 16,  # 16 GB
    'Disk Space': 100,  # 100 GB free
    'GPU': True  # Dedicated GPU
}

# Test if system specs can be detected
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
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

# Test if the validation for Unreal Engine 5 works
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_validate_specs():
    specs = check_system_specs()
    
    # Test for minimum requirements
    errors_min = validate_specs(specs, MINIMUM_REQUIREMENTS)
    assert isinstance(errors_min, list)

    # Test for recommended requirements
    errors_rec = validate_specs(specs, RECOMMENDED_REQUIREMENTS)
    assert isinstance(errors_rec, list)

# Skip GUI tests in headless environments
@pytest.mark.skipif("DISPLAY" not in os.environ, reason="Headless environment detected, skipping GUI test.")
@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_gui_creation():
    from main import create_gui
    try:
        create_gui()  # Attempt to create the GUI
    except Exception as e:
        pytest.fail(f"GUI creation failed: {e}")
