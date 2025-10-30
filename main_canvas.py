import tkinter as tk
from tkinter import messagebox, scrolledtext
import webbrowser
from PIL import Image, ImageTk
import subprocess
import os
import sys
import time
import shutil
import winreg
import ctypes
from tkextrafont import Font
from system_check import check_system_specs, check_driver_and_link_user
from validation import validate_specs


# Helper function to get the correct path when bundled with PyInstaller
def resource_path(relative_path):
    """Get the absolute path to the resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# Minimum driver versions for Unreal Engine
MINIMUM_DRIVER_VERSIONS = {
    "NVIDIA": "456.38",
    "AMD": "20.10.1",
    "Intel": "27.20.100.8587",
}

# Driver download links
DRIVER_DOWNLOAD_LINKS = {
    "NVIDIA": "https://www.nvidia.com/Download/index.aspx",
    "AMD": "https://www.amd.com/en/support",
    "Intel": "https://www.intel.com/content/www/us/en/download-center/home.html",
}

# Unreal Engine Requirements
REQUIREMENTS_UE5 = {
    "minimum": {"CPU": 2, "RAM": 4, "Disk Space": 100, "GPU": False},
    "recommended": {"CPU": 4, "RAM": 8, "Disk Space": 100, "GPU": True},
}

REQUIREMENTS_UE4 = {
    "minimum": {"CPU": 2, "RAM": 4, "Disk Space": 50, "GPU": False},
    "recommended": {"CPU": 4, "RAM": 8, "Disk Space": 50, "GPU": True},
}

INSTALL_PYTHON_VIDEO_WIN = "https://www.youtube.com/watch?v=cTwD_LC5F9A"
INSTALL_PYTHON_VIDEO_MAC = "https://www.youtube.com/watch?v=YigK5HwxV3M"
PYTHON_DOWNLOAD_LINK = "https://www.python.org/downloads/"

loading_overlay = None
loading_text = None


def show_loading_overlay(canvas: tk.Canvas, message="Loading..."):
    global loading_overlay, loading_text
    canvas.update_idletasks()  # Ensure canvas size is correct

    width = canvas.winfo_width()
    height = canvas.winfo_height()

    # Create gray overlay rectangle
    loading_overlay = canvas.create_rectangle(
        0, 0, width, height, fill="gray", stipple="gray75", tags="loading"
    )

    # Add loading text
    loading_text = canvas.create_text(
        width // 2,
        height // 2,
        text=message,
        fill="white",
        font=("Montserrat Black", 20),
        tags="loading",
    )

    canvas.update()


def hide_loading_overlay(canvas: tk.Canvas):
    canvas.delete("loading")


def set_widgets_state(parent: tk.Canvas, state):
    for widget in parent.winfo_children():
        try:
            widget.configure(state=state)
        except Exception:
            pass  # Not all widgets support 'state'


def find_vscode_executable():
    """
    Try to find VS Code. Returns an executable/command string or None.
    Checks: 'code' on PATH, common install locations, and Code.exe.
    """
    # If 'code' is on PATH, that's perfect for scripting later
    code_cmd = shutil.which("code")
    if code_cmd:
        return code_cmd

    # Windows common paths
    if os.name == "nt":
        # User-scope installs
        local = os.environ.get("LOCALAPPDATA")
        if local:
            user_code = os.path.join(local, "Programs", "Microsoft VS Code", "Code.exe")
            if os.path.isfile(user_code):
                return user_code

        # System-scope installs
        for base in (os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)")):
            if base:
                sys_code = os.path.join(base, "Microsoft VS Code", "Code.exe")
                if os.path.isfile(sys_code):
                    return sys_code

    return None

def is_vscode_installed():
    return find_vscode_executable() is not None

def install_vscode_with_winget(scope="user"):
    """
    Install VS Code via Winget. Returns True on success.
    Default scope='user' avoids needing admin. Valid: 'user' or 'machine'.
    """
    if os.name != "nt" or not is_winget_available():
        return False

    # Official Winget ID for Stable VS Code
    cmd = [
        "winget", "install",
        "-e", "--id", "Microsoft.VisualStudioCode",
        "--accept-package-agreements", "--accept-source-agreements",
        "--scope", scope,
        "--silent"
    ]

    messagebox.showinfo(
        "Installing VS Code",
        "Attempting to install Visual Studio Code via Winget.\n"
        "You may see a Windows prompt."
    )
    ok, out = _run(cmd)
    if not ok:
        # Retry without --silent; some environments/older App Installer versions reject it
        cmd2 = [c for c in cmd if c != "--silent"]
        ok2, out2 = _run(cmd2)
        ok, out = ok2, out2

    if ok:
        # Give PATH shims a moment to appear, then re-check
        for _ in range(6):
            time.sleep(2)
            if is_vscode_installed():
                return True

    # Surface useful output on failure
    messagebox.showerror(
        "VS Code Installation Failed",
        "Winget could not install VS Code automatically.\n\n"
        "Output:\n" + ((out or "")[-1200:] or "No output.")
    )
    return False

def ensure_vscode_available():
    """
    Ensure VS Code is installed; on Windows, attempt Winget install automatically.
    Returns the VS Code executable/command if available, else None.
    """
    exe = find_vscode_executable()
    if exe:
        return exe

    if os.name == "nt":
        if install_vscode_with_winget(scope="user"):
            return find_vscode_executable()

    # Non-Windows or Winget unavailable/failure -> None (caller can open download page)
    return None


def run_check_unreal_engine_compatibility(
    root, canvas, detail_button, detail_widget, test_mode=False
):
    set_widgets_state(root, "disabled")
    show_loading_overlay(canvas, "Checking system requirements...")

    check_unreal_engine_compatibility(detail_button, detail_widget, test_mode)

    hide_loading_overlay(canvas)
    set_widgets_state(root, "normal")


def check_unreal_engine_compatibility(detail_button, detail_widget, test_mode=False):
    """Check system compatibility with Unreal Engine and display results."""
    system_specs = check_system_specs()
    ue4_fallback = False
    detailed_info = "--- Current System Specs ---\n"

    for spec, value in system_specs.items():
        detailed_info += f"{spec}: {value}\n"

    detailed_info += "\n--- Unreal Engine 5 Requirements ---\n"
    detailed_info += f"Minimum: {REQUIREMENTS_UE5['minimum']}\n"
    detailed_info += f"Recommended: {REQUIREMENTS_UE5['recommended']}\n"

    validation_errors = validate_specs(system_specs, REQUIREMENTS_UE5["recommended"])

    if not validation_errors:
        result = "Your system meets Unreal Engine 5 recommended requirements!"
    else:
        validation_errors = validate_specs(system_specs, REQUIREMENTS_UE5["minimum"])
        if not validation_errors:
            result = "Your system meets Unreal Engine 5 minimum requirements."
        else:
            validation_errors_ue4 = validate_specs(
                system_specs, REQUIREMENTS_UE4["minimum"]
            )
            if not validation_errors_ue4:
                result = "Your system can run Unreal Engine 4, but not Unreal Engine 5."
                ue4_fallback = True
            else:
                result = "Your system cannot run Unreal Engine 4 or 5."
                validation_errors = validation_errors_ue4

    if test_mode:
        return result

    messagebox.showinfo("System Check Result", result)

    if validation_errors:
        detailed_info += "\n--- Validation Errors ---\n"
        for error in validation_errors:
            detailed_info += f"{error}\n"

    if ue4_fallback:
        detailed_info += "\n--- Unreal Engine 4 Fallback ---\n"
        detailed_info += (
            "Your system cannot run Unreal Engine 5, but it can run Unreal Engine 4.\n"
        )

    driver_message = check_driver_and_link_user()
    if driver_message:
        detailed_info += driver_message[1]
        if "outdated" in driver_message[0]:
            messagebox.showerror("Driver Guidance", driver_message[0])
        else:
            messagebox.showinfo("Driver Guidance", driver_message[0])

    detail_widget.config(state=tk.NORMAL)
    detail_widget.delete(1.0, tk.END)
    detail_widget.insert(tk.INSERT, detailed_info)
    detail_widget.config(state=tk.DISABLED)

    detail_button.pack(pady=10)


def run_setup_ai_ml_environment(root, canvas):
    if not is_python_installed():
        messagebox.showinfo(
            "Python Not Found",
            "Python is not installed. Please install Python first. Redirecting to installation page...",
        )
        webbrowser.open(PYTHON_DOWNLOAD_LINK)
        messagebox.showinfo(
            "How to video", "Here is a short video on how to install Python."
        )
        if os.name == "nt":
            webbrowser.open(INSTALL_PYTHON_VIDEO_WIN)
        else:
            webbrowser.open(INSTALL_PYTHON_VIDEO_MAC)
        messagebox.showinfo(
            "Re-try", "Click this button again after installing Python."
        )
        return
    
    set_widgets_state(root, "disabled")
    show_loading_overlay(canvas, "Setting up AI environment...")

    setup_ai_ml_environment()
    
    hide_loading_overlay(canvas)
    set_widgets_state(root, "normal")


def setup_ai_ml_environment():
    # Step 1: Check if we're in a risky directory
    current_path = os.path.abspath(".")
    risky_folders = ["desktop", "downloads", "temp"]
    if any(folder in current_path.lower() for folder in risky_folders):
        proceed = messagebox.askyesno(
            "Warning",
            "This folder doesn't look like a proper project location (e.g. it's on your Desktop or Downloads).\n\n"
            "It's best to move this folder somewhere like your Documents folder.\n\n"
            "Do you still want to continue?",
        )
        if not proceed:
            return

    # Step 2: Create virtual environment
    try:
        subprocess.run(["python", "-m", "venv", "venv"], check=True)
    except subprocess.CalledProcessError:
        try:
            subprocess.run(["python3", "-m", "venv", "venv"], check=True)
        except subprocess.CalledProcessError:
            messagebox.showerror(
                "Error",
                "Failed to create virtual environment.\nMake sure Python 3 is installed and available in PATH.",
            )
            return

    # Step 3: Activate and install requirements
    # NOTE: Activation is usually for terminal environments; here we just install using the correct pip
    pip_executable = (
        os.path.join("venv", "Scripts", "pip.exe")
        if os.name == "nt"
        else os.path.join("venv", "bin", "pip")
    )

    if not os.path.isfile("ai_requirements.txt"):
        messagebox.showerror(
            "Missing File",
            "Couldn't find ai_requirements.txt in the current directory.",
        )
        return

    try:
        subprocess.run(
            [pip_executable, "install", "-r", "ai_requirements.txt"], check=True
        )
        messagebox.showinfo(
            "Success", "Environment setup complete and requirements installed."
        )
    except subprocess.CalledProcessError:
        messagebox.showerror(
            "Installation Error", "Failed to install packages from ai_requirements.txt."
        )


def run_install_python_and_pygame(root, canvas):
    set_widgets_state(root, "disabled")
    show_loading_overlay(canvas, "Setting up Python...")

    install_python_and_pygame()

    hide_loading_overlay(canvas)
    set_widgets_state(root, "normal")


def install_python_and_pygame():
    """Check Python installation and install PyGame."""
    if not is_python_installed():
        install_python_with_winget()

    if is_python_installed():
        messagebox.showinfo("Python Found", "Python is installed. Installing PyGame...")
        install_pygame()
    else:
        messagebox.showinfo(
            "Python Not Found",
            "Python is not installed and automatic installation is unavailable.\n"
            "Redirecting to the official download page..."
        )
        messagebox.showinfo(
            "How to video", "Here is a short video on how to install Python."
        )
        webbrowser.open(PYTHON_DOWNLOAD_LINK)
        if os.name == "nt":
            webbrowser.open(INSTALL_PYTHON_VIDEO_WIN)
        else:
            webbrowser.open(INSTALL_PYTHON_VIDEO_MAC)
        


def is_python_installed():
    """Check if Python is installed on the system."""
    try:
        subprocess.run(
            ["python", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return True
    except Exception:
        try:
            subprocess.run(
                ["python3", "--version"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return True
        except Exception:
            return False     
        
 
def _run(cmd):
    """Run a command, return (ok, stdout+stderr)."""
    try:
        cp = subprocess.run(cmd, check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return cp.returncode == 0, (cp.stdout or "")
    except Exception as e:
        return False, str(e)  


def is_winget_available():
    if os.name != "nt":
        return False
    ok, _out = _run(["winget", "--version"])
    return ok


def refresh_path_from_registry():
    """Pull latest PATH from Windows registry into current process env."""
    paths = []

    # Machine-wide PATH
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment") as key:
            paths.append(winreg.QueryValueEx(key, "Path")[0])
    except FileNotFoundError:
        pass

    # User-specific PATH
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"Environment") as key:
            paths.append(winreg.QueryValueEx(key, "Path")[0])
    except FileNotFoundError:
        pass

    combined = ";".join(paths)
    if combined:
        os.environ["PATH"] = combined


def broadcast_env_change():
    """Notify Windows that environment variables have changed."""
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    SMTO_ABORTIFHUNG = 0x0002
    res = ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST,
        WM_SETTINGCHANGE,
        0,
        "Environment",
        SMTO_ABORTIFHUNG,
        5000,
        None
    )
    return res != 0


def refresh_windows_path():
    """
    Refresh PATH in the current Python process and notify Windows
    after a new software install (like Python via Winget).
    """
    if os.name != "nt":
        return

    try:
        refresh_path_from_registry()
        broadcast_env_change()
        print("[✓] PATH refreshed successfully.")
    except Exception as e:
        print(f"[!] Failed to refresh PATH: {e}")


def install_python_with_winget(package_id="Python.Python.3.12", retries=1):
    """
    Try to install Python via Winget.
    Returns True on success, False on failure.
    """
    if os.name != "nt":
        return False
    if not is_winget_available():
        return False

    # Best practice flags:
    # -e exact id, accept agreements, try silent
    cmd = [
        "winget", "install",
        "-e", "--id", package_id,
        "--accept-package-agreements",
        "--accept-source-agreements",
        #"--silent"
    ]
    messagebox.showinfo("Installing Python", "Attempting to install Python automatically via Winget. "
                                             "You may be prompted by Windows.")
    ok, out = _run(cmd)
    # if not ok:
    #     # Some systems dislike --silent; try without it once
    #     if retries > 0:
    #         cmd2 = [c for c in cmd if c != "--silent"]
    #         ok2, out2 = _run(cmd2)
    #         ok, out = ok2, out2

    # Give the system a moment to update PATH/registry shims
    if ok:
        refresh_windows_path()
        for _ in range(6):
            time.sleep(2)
            if is_python_installed():
                return True
            
        # Python may be installed but PATH not updated, restarting app seems to fix
        messagebox.showinfo(
                "Restart Required",
                "Python was installed, but Windows hasn't exposed it to this session yet.\n\n"
                "Please restart this tool and select the same button continue."
            )
        quit() # Closes window without return, leaves loading screen to hang forever
        sys.exit()
    

    # If it still failed, surface output to help users
    messagebox.showerror("Python Installation Failed",
                         "Winget could not install Python automatically.\n\n"
                         "Output:\n" + (out[-1200:] if out else "No output."))
    return False


def install_pygame():
    """Install PyGame using pip."""
    try:
        python_exec = "python" if getattr(sys, "frozen", False) else sys.executable
        subprocess.run([python_exec, "-m", "pip", "install", "pygame"], check=True)
        messagebox.showinfo("PyGame Installation", "PyGame installed successfully!")
    except subprocess.CalledProcessError:
        messagebox.showerror(
            "Installation Failed", "Failed to install PyGame. Try manually."
        )
        webbrowser.open("https://www.pygame.org/wiki/GettingStarted")


def toggle_details_view(widget, button):
    """Toggle visibility of detailed information widget."""
    if widget.winfo_viewable():
        widget.pack_forget()
        button.config(text="Show Advanced Information")
    else:
        widget.pack(pady=10)
        button.config(text="Hide Advanced Information")


def create_multiline_button(
    canvas: tk.Canvas,
    x,
    y,
    lines,
    colors,
    fonts,
    command,
    width,
    height,
    bg_color,
    spacing,
):
    """Create a multiline styled button on a canvas."""
    padding = 10
    button_tag = f"button_{x}_{y}"

    canvas.create_rectangle(
        x, y, x + width, y + height, fill=bg_color, outline=bg_color, tags=button_tag
    )

    for i, (line, color, font) in enumerate(zip(lines, colors, fonts)):
        canvas.create_text(
            x + padding,
            y + padding + i * spacing,
            text=line,
            fill=color,
            font=font,
            anchor="nw",
            tags=button_tag,
        )

    canvas.tag_bind(button_tag, "<Button-1>", lambda event: command())


def create_gui():
    """Create the main GUI window."""
    root = tk.Tk()
    root.title("Software Academy - System Checker & Python Installer")

    favicon = ImageTk.PhotoImage(
        Image.open(resource_path("images/favicon.ico")).resize(
            (32, 32), Image.Resampling.BILINEAR
        )
    )
    root.iconphoto(False, favicon)

    academy_color = "#00aeff"
    frame = tk.Frame(root, bg="white")
    frame.pack(padx=20, pady=20)

    logo = ImageTk.PhotoImage(
        Image.open(resource_path("images/logo.png")).resize(
            (200, 43), Image.Resampling.BILINEAR
        )
    )
    tk.Label(frame, image=logo, bg="white").pack(anchor="nw")

    # Load in the font for TK (??SUPER WEIRD??)
    mon_font = Font(file=resource_path("fonts/Montserrat-Black.ttf"))

    canvas = tk.Canvas(frame, bg="white", width=720, height=280, highlightthickness=0)
    canvas.pack()

    create_multiline_button(
        canvas,
        20,
        80,
        ["Unreal Engine", "Hardware Checker >"],
        ["#FFFFFF", "#000040"],
        [("Montserrat Black", 24), ("Montserrat Black", 18)],
        lambda: run_check_unreal_engine_compatibility(
            root, canvas, details_button, detail_widget
        ),
        290,
        85,
        "#FF076B",
        35,
    )

    create_multiline_button(
        canvas,
        403,
        80,
        ["Python", "              Installation >"],
        ["#FFFFFF", "#000040"],
        [("Montserrat Black", 24), ("Montserrat Black", 18)],
        lambda: run_install_python_and_pygame(root, canvas),
        290,
        85,
        "#00AEFF",
        35,
    )

    create_multiline_button(
        canvas,
        20,
        180,
        ["AI & Machine Learning", "Setup Environment >"],
        ["#FFFFFF", "#000040"],
        [("Montserrat Black", 24), ("Montserrat Black", 18)],
        lambda: run_setup_ai_ml_environment(root, canvas),
        673,
        85,
        "#3CFF8F",
        35,
    )

    detail_widget = scrolledtext.ScrolledText(
        frame, wrap=tk.WORD, width=60, height=15, state=tk.DISABLED
    )

    details_button = tk.Button(
        frame,
        text="Show Advanced Information",
        command=lambda: toggle_details_view(detail_widget, details_button),
        font=("Montserrat Black", 12),
        bg=academy_color,
        fg="white",
        borderwidth=0,
    )
    details_button.pack_forget()

    root.configure(bg="white")
    root.mainloop()


if __name__ == "__main__":
    create_gui()
