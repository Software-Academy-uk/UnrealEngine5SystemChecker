import tkinter as tk
from tkinter import messagebox
import webbrowser
from PIL import Image, ImageTk

from system_check import check_system_specs
from validation import validate_specs

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

# Function to display Unreal Engine test results in a messagebox
def test_unreal_engine():
    specs = check_system_specs()

    # First, check against Unreal Engine 5 recommended requirements
    validation_errors = validate_specs(specs, RECOMMENDED_REQUIREMENTS)

    if not validation_errors:
        output = "Yes, your system can run Unreal Engine 5!"
    else:
        # If recommended fails, check against minimum
        validation_errors = validate_specs(specs, MINIMUM_REQUIREMENTS)
        if not validation_errors:
            output = "Your system meets the minimum requirements for Unreal Engine 5, but may not perform optimally."
        else:
            # If minimum requirements fail, suggest Unreal Engine 4
            if specs['RAM'] >= 8:
                output = "Your system doesn't meet Unreal Engine 5 requirements, but you can run Unreal Engine 4."
            else:
                output = "No, your system cannot run Unreal Engine 4 or 5."

    # Display results in a messagebox
    messagebox.showinfo("System Check Result", output)

# Function to install Python and PyGame
def install_python_pygame():
    messagebox.showinfo("Python & PyGame Installation", "Opening links to download Python and PyGame...")
    # Open download links in the web browser
    webbrowser.open("https://www.python.org/downloads/")
    webbrowser.open("https://www.pygame.org/wiki/GettingStarted")

# Creating the GUI window
def create_gui():
    root = tk.Tk()

    # Update the main window title
    root.title("Software Academy - System Checker & Python Installer")

    # Load and set the favicon (small logo) image
    favicon = Image.open("images/software-academy-favicon_32x32.png")
    favicon = favicon.resize((32, 32))
    favicon = ImageTk.PhotoImage(favicon)

    # Set window icon (favicon)
    root.iconphoto(False, favicon)

    # Use the academy color for styling
    academy_color = "#00aeff"

    # Create a frame for better alignment and cleaner layout
    frame = tk.Frame(root, bg="white")
    frame.pack(padx=20, pady=20)

    # Display the full logo in the window
    logo = Image.open("images/software-academy-logo-image.png")
    logo = ImageTk.PhotoImage(logo)
    
    logo_label = tk.Label(frame, image=logo, bg="white")
    logo_label.image = logo  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=10)

    # Title text (update to reflect both Unreal Engine check and Python/PyGame install)
    title = tk.Label(frame, text="System Checker & Python/PyGame Installer", font=("Helvetica", 16, "bold"), fg=academy_color, bg="white")
    title.pack(pady=10)

    # Instructions text (reflect dual functionality)
    instructions = tk.Label(frame, text="Choose an option below to check system requirements or install Python & PyGame.", font=("Helvetica", 12), bg="white")
    instructions.pack(pady=10)

    # Create a frame for the buttons to place them side by side
    button_frame = tk.Frame(frame, bg="white")
    button_frame.pack(pady=10)

    # Button to check Unreal Engine system requirements
    check_button = tk.Button(button_frame, text="Test hardware for Unreal Engine", command=test_unreal_engine, font=("Helvetica", 12), bg=academy_color, fg="white")
    check_button.pack(side=tk.LEFT, padx=10)

    # Button to install Python and PyGame
    python_button = tk.Button(button_frame, text="Install Python & PyGame", command=install_python_pygame, font=("Helvetica", 12), bg=academy_color, fg="white")
    python_button.pack(side=tk.LEFT, padx=10)

    # Set a white background for the entire window
    root.configure(bg="white")

    root.mainloop()

if __name__ == "__main__":
    # Run the GUI
    create_gui()
