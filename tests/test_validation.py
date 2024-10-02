import pytest
from validation import validate_specs

# Test valid specs for Unreal Engine 5 recommended requirements
def test_validate_ue5_recommended():
    specs = {
        'CPU': '4 cores',
        'RAM': '8 GB',
        'Disk Space': '100 GB free',
        'GPU': 'Dedicated GPU'
    }
    requirements = {
        'CPU': 4,
        'RAM': 8,
        'Disk Space': 100,
        'GPU': True
    }
    errors = validate_specs(specs, requirements)
    assert len(errors) == 0

# Test valid specs for Unreal Engine 5 minimum requirements
def test_validate_ue5_minimum():
    specs = {
        'CPU': '2 cores',
        'RAM': '4 GB',
        'Disk Space': '100 GB free',
        'GPU': 'No dedicated GPU'
    }
    requirements = {
        'CPU': 2,
        'RAM': 4,
        'Disk Space': 100,
        'GPU': False
    }
    errors = validate_specs(specs, requirements)
    assert len(errors) == 0

# Test invalid CPU specs
def test_invalid_cpu():
    specs = {
        'CPU': '2 cores',
        'RAM': '8 GB',
        'Disk Space': '150 GB free',
        'GPU': 'Dedicated GPU'
    }
    requirements = {
        'CPU': 4,
        'RAM': 8,
        'Disk Space': 100,
        'GPU': True
    }
    errors = validate_specs(specs, requirements)
    assert "CPU does not meet the requirement" in errors[0]
