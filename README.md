## Unreal Engine System Checker and Python/PyGame Installer

This tool helps users determine if their system can run **Unreal Engine 4** or **Unreal Engine 5**, checks GPU drivers to ensure they are up to date, and provides an option to install **Python** and **PyGame**. It is designed to be user-friendly, especially for parents who may be unfamiliar with technical requirements.

### Features:
1. **System Check for Unreal Engine**:
   - Determines if the system meets the **minimum** and **recommended** requirements for **Unreal Engine 5**.
   - If the system cannot run **Unreal Engine 5**, it checks if the system can run **Unreal Engine 4**.
   - Displays detailed information on why the system may fail and suggests fallback options if applicable.

2. **Driver Check**:
   - Detects the user's **GPU** and verifies if the GPU drivers are up to date.
   - Provides links to download the latest drivers from NVIDIA, AMD, or Intel based on the detected GPU.
   - Warns the user if their drivers are outdated or missing.

3. **Python & PyGame Installation**:
   - Automatically installs **PyGame** if Python is detected on the system.
   - If Python is not installed, the user is directed to the official Python download page.
   - Additionally, a helpful video link is provided to guide users through the installation process.

### System Requirements for Unreal Engine:
- **Minimum Requirements for Unreal Engine 5**:
  - **CPU**: 2 cores
  - **RAM**: 4 GB
  - **Disk Space**: 100 GB free
  - **GPU**: No dedicated GPU required

- **Recommended Requirements for Unreal Engine 5**:
  - **CPU**: 4 cores
  - **RAM**: 8 GB
  - **Disk Space**: 100 GB free
  - **GPU**: Dedicated GPU required

- **Minimum Requirements for Unreal Engine 4**:
  - **CPU**: 2 cores
  - **RAM**: 4 GB
  - **Disk Space**: 50 GB free
  - **GPU**: No dedicated GPU required

- **Recommended Requirements for Unreal Engine 4**:
  - **CPU**: 4 cores
  - **RAM**: 8 GB
  - **Disk Space**: 50 GB free
  - **GPU**: Dedicated GPU required

### Usage Instructions:

1. **Running the System Checker**:
   - When the application is launched, you will see two buttons:
     - **Test hardware for Unreal Engine**: This will test your system’s compatibility with Unreal Engine 5 and 4.
     - **Install Python & PyGame**: This installs Python and PyGame if Python is already installed on your system.

2. **Advanced Information**:
   - After running the system test, you can click the **Show Advanced Information** button to display detailed system specs, including why the system may have failed the Unreal Engine check.

3. **Driver Update Guidance**:
   - The program will automatically check your GPU driver version. If the drivers are outdated or missing, a warning will be displayed, and a link to download the latest drivers from the appropriate vendor will be provided.

### How to Install:
1. Clone the repository:
   ```bash
   git clone https://github.com/Software-Academy-uk/UnrealEngine5SystemChecker
   ```
2. Navigate to the project folder:
   ```bash
   cd UnrealEngine5SystemChecker
   ```
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

### How to Test:
Unit tests are provided to ensure the functionality of the system checker and Python/PyGame installer. Tests are split across multiple files for modularity, and they can be run using `pytest`.

1. Install testing dependencies:
   ```bash
   pip install pytest
   ```

2. Run the tests:
   ```bash
   pytest
   ```

3. Test categories:
   - **Unreal Engine System Tests**: Located in the `unreal_engine_tests` folder, these tests check various system configurations against the Unreal Engine requirements.
   - **Python & PyGame Installer Tests**: Located in `test_python_pygame.py`, these tests verify the Python detection and PyGame installation process.
   - **Driver Check Tests**: Located in `test_driver_guidance.py`, these tests ensure GPU detection and driver guidance functionality.

### License:
This tool is licensed to Software Academy and cannot be redistributed or modified without permission.