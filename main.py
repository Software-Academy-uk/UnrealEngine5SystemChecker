from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import psutil
import platform
import shutil
import GPUtil

# Function to check if a dedicated GPU is present
def check_gpu():
    gpus = GPUtil.getGPUs()
    if not gpus:
        return "No dedicated GPU found"
    else:
        return f"Dedicated GPU found: {gpus[0].name}"

# Adding GPU check to system specs
def check_system_specs():
    specs = {}

    # CPU
    cpu_info = platform.processor()
    cpu_cores = psutil.cpu_count(logical=False)  # Physical cores
    specs['CPU'] = f"{cpu_info} ({cpu_cores} cores)"

    # RAM
    ram = round(psutil.virtual_memory().total / (1024 ** 3), 2)  # Convert to GB
    specs['RAM'] = f"{ram} GB"

    # Disk space
    total, used, free = shutil.disk_usage('/')
    free_gb = round(free / (1024 ** 3), 2)  # Convert to GB
    specs['Disk Space'] = f"{free_gb} GB free"

    # OS
    os_info = platform.system() + " " + platform.release()
    specs['OS'] = os_info

    # GPU
    gpu_info = check_gpu()
    specs['GPU'] = gpu_info

    return specs

# Function to validate system specs for Unreal Engine 5
def validate_specs(specs):
    validation_results = []

    # CPU: 4 cores minimum
    cpu_cores = int(specs['CPU'].split('(')[-1].split(' ')[0])
    if cpu_cores < 4:
        validation_results.append("CPU does not meet the requirement (at least 4 cores).")

    # RAM: 16 GB minimum
    ram = float(specs['RAM'].split(' ')[0])
    if ram < 16:
        validation_results.append("Not enough RAM (at least 16 GB required).")

    # Disk Space: 50 GB minimum free space
    free_disk = float(specs['Disk Space'].split(' ')[0])
    if free_disk < 50:
        validation_results.append("Not enough disk space (at least 50 GB required).")

    # GPU: Must have a dedicated GPU
    if "No dedicated GPU" in specs['GPU']:
        validation_results.append("No dedicated GPU found (required for Unreal Engine 5).")

    return validation_results

# Function to display results in the GUI
def display_results(specs):
    validation_errors = validate_specs(specs)

    if not validation_errors:
        messagebox.showinfo("System Check", "Yes, your system can run Unreal Engine 5!")
    else:
        messagebox.showerror("System Check", "No, your system cannot run Unreal Engine 5.\n\n" + "\n".join(validation_errors))

# Function to initiate the system check and GUI
def run_gui_system_check():
    specs = check_system_specs()  # Get system specs
    display_results(specs)        # Show results in GUI

# Creating the GUI window
def create_gui():
    root = tk.Tk()
    root.title("Software Academy - Unreal Engine 5 System Checker")

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

    # Title text
    title = tk.Label(frame, text="Unreal Engine 5 System Checker", font=("Helvetica", 16, "bold"), fg=academy_color, bg="white")
    title.pack(pady=10)

    # Instructions text
    instructions = tk.Label(frame, text="Click the button below to check if your system meets Unreal Engine 5 requirements.", font=("Helvetica", 12), bg="white")
    instructions.pack(pady=10)

    # Check system button
    check_button = tk.Button(frame, text="Check System", command=run_gui_system_check, font=("Helvetica", 12), bg=academy_color, fg="white")
    check_button.pack(pady=20)

    # Set a white background for the entire window
    root.configure(bg="white")

    root.mainloop()

if __name__ == "__main__":
    # Run the GUI
    create_gui()
