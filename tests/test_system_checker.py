import pytest
from main import check_system_specs

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