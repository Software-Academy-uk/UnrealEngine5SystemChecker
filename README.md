# Unreal Engine 5 System Checker

This is a simple tool that checks if a system can run Unreal Engine 5 based on CPU, RAM, disk space, and GPU.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the program:
   ```bash
   python main.py
   ```

## Packaging as an Executable (Optional)

If you'd like to convert this to an executable:
```bash
pyinstaller --onefile --windowed main.py
```

## Requirements
- Python 3.x
- psutil
- GPUtil
- tkinter