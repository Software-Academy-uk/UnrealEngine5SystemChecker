# System Checker & Python/PyGame Installer

This tool helps check whether your system meets the hardware requirements for Unreal Engine 5 and can also guide you through installing Python and PyGame.

## Features
- **Unreal Engine 5 System Requirements Checker**: Detects if your system meets both the minimum and recommended requirements for Unreal Engine 5. It will suggest Unreal Engine 4 if your system doesn't meet Unreal Engine 5's requirements but can still run Unreal Engine 4.
- **Python & PyGame Installer**: Provides easy links to install Python and PyGame if needed.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/your-repo-name.git
    ```

2. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the tool:
    ```bash
    python main.py
    ```

## Usage
- **Test Hardware for Unreal Engine**: Click the "Test hardware for Unreal Engine" button to check if your system can run Unreal Engine 5 or Unreal Engine 4.
- **Install Python & PyGame**: Click the "Install Python & PyGame" button to be guided through the installation process.

## Requirements
- Python 3.x
- The following Python libraries:
  - `psutil`
  - `GPUtil`
  - `tkinter` (for GUI)
  - `Pillow` (for image handling)

## Notes
- Ensure your system has a dedicated GPU for Unreal Engine 5.