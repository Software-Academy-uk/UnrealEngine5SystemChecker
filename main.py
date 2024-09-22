import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from system_check import check_system_specs
from validation import validate_specs

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
