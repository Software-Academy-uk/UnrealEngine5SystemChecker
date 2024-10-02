import pytest
from unittest.mock import patch, MagicMock
from main import driver_guidance

@patch('GPUtil.getGPUs')
def test_nvidia_driver_guidance(mock_get_gpus):
    # Mock GPU to simulate an NVIDIA GPU
    mock_gpu = MagicMock()
    mock_gpu.name = "NVIDIA GTX 1080"
    mock_gpu.driver = "456.71"
    mock_get_gpus.return_value = [mock_gpu]
    
    guidance = driver_guidance()
    assert "NVIDIA" in guidance
    assert "https://www.nvidia.com" in guidance

@patch('GPUtil.getGPUs')
def test_no_gpu_detected(mock_get_gpus):
    mock_get_gpus.return_value = []
    
    guidance = driver_guidance()
    assert "No GPU detected" in guidance
