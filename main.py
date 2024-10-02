import tkinter as tk
from tkinter import messagebox, scrolledtext
import webbrowser
from PIL import Image, ImageTk
import subprocess
import sys

from system_check import check_system_specs, driver_guidance
from validation import validate_specs

# Unreal Engine Requirements (Minimum, Recommended, and Unreal Engine 4)
MINIMUM_REQUIREMENTS_UE5 = {
    'CPU': 2,   # 2 cores
    'RAM': 4,   # 4 GB
    'Disk Space': 100,  # 100 GB free
    'GPU': False  # Dedicated GPU not required
}

RECOMMENDED_REQUIREMENTS_UE5 = {
    'CPU': 4,   # 4 cores or more
    'RAM': 8,   # 8 GB
    'Disk Space': 100,  # 100 GB free
    'GPU': True  # Dedicated GPU required
}

MINIMUM_REQUIREMENTS_UE4 = {
    'CPU': 2,   # 2 cores
    'RAM': 4,   # 4 GB
    'Disk Space': 50,   # 50 GB free
    'GPU': False  # Dedicated GPU not required
}

RECOMMENDED_REQUIREMENTS_UE4 = {
    'CPU': 4,   # 4 cores or more
    'RAM': 8,   # 8 GB
    'Disk Space': 50,   # 50 GB free
    'GPU': True  # Dedicated GPU required
}


def test_unreal_engine(detailed_button, detailed_widget, is_testing=False):
    """Display Unreal Engine test results and show detailed information, including driver guidance."""
    specs = check_system_specs()
    ue4_fallback = False  # To track if UE4 is selected as fallback
    detailed_info = "--- Current System Specs ---\n"
    
    # Add current system specs to the detailed info
    for key, value in specs.items():
        detailed_info += f"{key}: {value}\n"

    detailed_info += "\n--- Unreal Engine 5 Requirements ---\n"
    detailed_info += f"Minimum Requirements: {MINIMUM_REQUIREMENTS_UE5}\n"
    detailed_info += f"Recommended Requirements: {RECOMMENDED_REQUIREMENTS_UE5}\n"
    
    # First, check against Unreal Engine 5 recommended requirements
    validation_errors = validate_specs(specs, RECOMMENDED_REQUIREMENTS_UE5)

    if not validation_errors:
        output = "Yes, your system can run Unreal Engine 5!"
    else:
        # If recommended fails, check against minimum UE5
        validation_errors = validate_specs(specs, MINIMUM_REQUIREMENTS_UE5)
        if not validation_errors:
            output = ("Your system meets the minimum requirements for Unreal Engine 5, "
                      "but may not perform optimally.")
        else:
            # If UE5 minimum requirements fail, check for Unreal Engine 4
            validation_errors_ue4 = validate_specs(specs, MINIMUM_REQUIREMENTS_UE4)
            if not validation_errors_ue4:
                output = "Your system can run Unreal Engine 4, but not Unreal Engine 5."
                ue4_fallback = True  # Mark that UE4 fallback was selected
            else:
                output = "No, your system cannot run Unreal Engine 4 or 5."
                validation_errors = validation_errors_ue4  # Use UE4 errors if UE5 failed
                
    # If running tests, return the output instead of showing a messagebox
    if is_testing:
        return output
    else:
        # Show result in messagebox
        messagebox.showinfo("System Check Result", output)

    # Append validation errors to the detailed info
    if validation_errors:
        detailed_info += "\n--- Validation Errors ---\n"
        for error in validation_errors:
            detailed_info += f"{error}\n"

    # Show UE4 fallback in the detailed info if selected
    if ue4_fallback:
        detailed_info += ("\n--- Unreal Engine 4 Fallback ---\n"
                          "Your system cannot run Unreal Engine 5, but it can run Unreal Engine 4.\n")

    # Check for driver guidance
    driver_message = driver_guidance()
    if "Error" in driver_message or "Please" in driver_message:
        messagebox.showwarning("Driver Guidance", driver_message)

    # Update the detailed widget with system specs and errors
    detailed_widget.config(state=tk.NORMAL)  # Enable editing to update content
    detailed_widget.delete(1.0, tk.END)  # Clear previous content
    detailed_widget.insert(tk.INSERT, detailed_info)  # Add new content
    detailed_widget.config(state=tk.DISABLED)  # Disable editing

    # Show the "Show Advanced Information" button after the test is run
    detailed_button.pack(pady=10)
    


def install_python_pygame():
    """Check if Python is installed and install PyGame."""
    python_installed = check_python_installed()

    if python_installed:
        messagebox.showinfo("Python Found", "Python is installed on your system. "
                                            "Proceeding to install PyGame.")
        install_pygame()  # Auto-install PyGame using pip
    else:
        messagebox.showinfo("Python Not Found", "Python is not installed on your system. "
                                                "Please install Python first.")
        webbrowser.open("https://www.python.org/downloads/")
        messagebox.showinfo("How to video", "Here is a short video on how to install Python.")
        webbrowser.open("https://www.youtube.com/watch?v=cTwD_LC5F9A")


def check_python_installed():
    """Check if Python is installed."""
    try:
        subprocess.run([sys.executable, '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception:
        return False


def install_pygame():
    """Install PyGame using pip."""
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pygame"], check=True)
        messagebox.showinfo("PyGame Installation", "PyGame has been successfully installed!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Installation Failed", "Failed to install PyGame. Please try manually.")
        webbrowser.open("https://www.pygame.org/wiki/GettingStarted")


def toggle_detailed_view(detailed_widget, details_button):
    """Toggle the visibility of the detailed view and update button text."""
    if detailed_widget.winfo_viewable():
        detailed_widget.pack_forget()  # Hide the detailed view
        details_button.config(text="Show Advanced Information")  # Update button text to "Show"
    else:
        detailed_widget.pack(pady=10)  # Show the detailed view
        details_button.config(text="Hide Advanced Information")  # Update button text to "Hide"


def create_gui():
    """Create the GUI window."""
    root = tk.Tk()

    root.title("Software Academy - System Checker & Python Installer")

    # Load and set the favicon (small logo) image
    favicon = Image.open("images/software-academy-favicon_32x32.png")
    favicon = favicon.resize((32, 32))
    favicon = ImageTk.PhotoImage(favicon)

    # Set window icon (favicon)
    root.iconphoto(False, favicon)

    academy_color = "#00aeff"  # Academy color for styling

    frame = tk.Frame(root, bg="white")
    frame.pack(padx=20, pady=20)

    # Display the full logo in the window
    logo = Image.open("images/software-academy-logo-image.png")
    logo = ImageTk.PhotoImage(logo)
    
    logo_label = tk.Label(frame, image=logo, bg="white")
    logo_label.image = logo  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=10)

    # Title text (reflect dual functionality)
    title = tk.Label(frame, text="System Checker & Python/PyGame Installer",
                     font=("Helvetica", 16, "bold"), fg=academy_color, bg="white")
    title.pack(pady=10)

    instructions = tk.Label(frame, text="Choose an option below to check system requirements or install Python & PyGame.",
                            font=("Helvetica", 12), bg="white")
    instructions.pack(pady=10)

    button_frame = tk.Frame(frame, bg="white")
    button_frame.pack(pady=10)

    # Button to check Unreal Engine system requirements
    check_button = tk.Button(button_frame, text="Test hardware for Unreal Engine",
                             command=lambda: test_unreal_engine(details_button, detailed_widget),
                             font=("Helvetica", 12), bg=academy_color, fg="white")
    check_button.pack(side=tk.LEFT, padx=10)

    # Button to install Python and PyGame
    python_button = tk.Button(button_frame, text="Install Python & PyGame",
                              command=install_python_pygame, font=("Helvetica", 12),
                              bg=academy_color, fg="white")
    python_button.pack(side=tk.LEFT, padx=10)

    # Detailed output box (initially hidden)
    detailed_widget = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=60, height=15, state=tk.DISABLED)
    
    details_button = tk.Button(frame, text="Show Advanced Information",
                               command=lambda: toggle_detailed_view(detailed_widget, details_button),
                               font=("Helvetica", 12), bg=academy_color, fg="white")
    details_button.pack_forget()  # Initially hidden

    root.configure(bg="white")

    root.mainloop()


if __name__ == "__main__":
    create_gui()
