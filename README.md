# Unreal Engine System Checker

This tool checks whether your system meets the hardware requirements for Unreal Engine 5 and can also guide you through installing Python and PyGame.

## Features
- **Unreal Engine 5 System Requirements Checker**: Detects if your system meets both the minimum and recommended requirements for Unreal Engine 5.
- **Python & PyGame Installer**: Provides easy links to install Python and PyGame if needed.

## Setup and Installation

### 1. Clone the repository:
   ```bash
   git clone https://github.com/William-Nitrosis/UnrealEngine5SystemChecker.git
   cd UnrealEngine5SystemChecker
   ```

### 2. Set up a Python Virtual Environment (Recommended):
To avoid dependency clashes, it's recommended to run the tool within a Python virtual environment.

   - **For Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     ```

   - **For macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

### 3. Install the Required Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 4. Running the Tool:
Once all dependencies are installed, you can run the tool:
   ```bash
   python main.py
   ```

### 5. Exiting the Virtual Environment:
When you're done using the tool, deactivate the virtual environment by running:
   ```bash
   deactivate
   ```

## Running Tests

There are multiple test cases designed to check different hardware configurations. However, due to mock state leakage between tests when run in bulk, it is recommended to run individual tests.

### Running Individual Tests

You can run specific tests by using pytest with markers:

- **Test for fully passing Unreal Engine 5 (Recommended)**:
  ```bash
  pytest -m pass_ue5
  ```

- **Test for passing Unreal Engine 5 (Minimum)**:
  ```bash
  pytest -m min_pass_ue5
  ```

- **Test for failing Unreal Engine 5 but passing Unreal Engine 4 (Recommended)**:
  ```bash
  pytest -m fail_ue5_pass_ue4
  ```

- **Test for failing Unreal Engine 5 but passing Unreal Engine 4 (Minimum)**:
  ```bash
  pytest -m fail_ue5_min_pass_ue4
  ```

- **Test for failing both Unreal Engine 5 and Unreal Engine 4**:
  ```bash
  pytest -m fail_ue5_fail_ue4
  ```

### Known Issue

Running all tests together using `pytest` might cause mock state leakage between tests, resulting in failures. To avoid this issue, run tests individually as described above.

## Requirements
- Python 3.x
- The following Python libraries:
  - `psutil`
  - `GPUtil`
  - `tkinter` (for GUI)
  - `Pillow` (for image handling)

## Notes
- Ensure your system has a dedicated GPU for Unreal Engine 5.