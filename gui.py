import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os

# Current working directory
current_working_dir = os.getcwd()

# Sorting options
SORT_OPTIONS = {
    "None": "",
    "Top Processes (-p)": "-p",
    "Sort by CPU (-c)": "-c",
    "Sort by Memory (-m)": "-m",
    "Sort by Disk (-d)": "-d",
    "Sort by Network (-n)": "-n",
}

def execute_list_windows():
    """Run the List Windows command with selected options."""
    selected_option = sort_var.get()
    additional_args = []
    if SORT_OPTIONS[selected_option]:  # If a valid sort option is chosen
        additional_args.append(SORT_OPTIONS[selected_option])

    # Check for significant digits
    if shorten_digits_var.get() == "Yes":
        try:
            significant_digits = int(input_significant_digits.get())
            additional_args += ["-sd", str(significant_digits)]
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number for significant digits.")
            return

    # Run the listWindows.py script with the selected options
    try:
        subprocess.run(["python", "listWindows.py"] + additional_args)

        # Open output.txt if the checkbox is selected
        if open_output_var.get():
            output_path = os.path.join(current_working_dir, "output.txt")
            if os.path.exists(output_path):
                subprocess.Popen(["Notepad", output_path], shell=True)  # Open output.txt using Notepad
            else:
                messagebox.showerror("Error", f"Output file not found at {output_path}")
    except Exception as e:
        messagebox.showerror("Execution Error", f"An error occurred: {str(e)}")

def execute_open_windows():
    """Run the Open Windows command with user inputs."""
    try:
        filename = input_filename.get()
        num_windows = int(input_num_windows.get())
        viewer = input_viewer.get()
        subprocess.run(["python", "openwindows.py", filename, str(num_windows), viewer])
    except Exception as e:
        messagebox.showerror("Execution Error", f"An error occurred: {str(e)}")

def update_working_dir():
    """Update the displayed working directory."""
    lbl_working_dir.config(text=f"Current Directory: {current_working_dir}")

def change_working_dir():
    """Change the working directory."""
    global current_working_dir
    new_dir = filedialog.askdirectory(initialdir=current_working_dir)
    if new_dir:
        os.chdir(new_dir)  # Change the working directory
        current_working_dir = os.getcwd()  # Update the global variable
        update_working_dir()
        messagebox.showinfo("Directory Changed", f"Working directory changed to:\n{current_working_dir}")

def exit_program():
    """Exit the program."""
    root.destroy()

# Initialize main window
root = tk.Tk()
root.title("Random Tools GUI")
root.geometry("500x600")

# Add buttons and inputs
tk.Label(root, text="Random Tools Manager", font=("Helvetica", 16)).pack(pady=10)

# Section: Working Directory
tk.Label(root, text="Manage Working Directory", font=("Helvetica", 14)).pack(pady=10)
lbl_working_dir = tk.Label(root, text=f"Current Directory: {current_working_dir}", wraplength=400, justify="center")
lbl_working_dir.pack(pady=5)
tk.Button(root, text="Change Working Directory", command=change_working_dir, width=25).pack(pady=5)

# Section: List Windows
tk.Label(root, text="List Windows", font=("Helvetica", 14)).pack(pady=10)

# Dropdown for sorting options
tk.Label(root, text="Sorting Options:").pack()
sort_var = tk.StringVar(root)
sort_var.set("None")  # Default value
tk.OptionMenu(root, sort_var, *SORT_OPTIONS.keys()).pack(pady=5)

# Significant Digits Options
tk.Label(root, text="Shorten Significant Digits:").pack()
shorten_digits_var = tk.StringVar(root)
shorten_digits_var.set("No")  # Default value
tk.OptionMenu(root, shorten_digits_var, "No", "Yes").pack(pady=5)

# Input for significant digits (hidden by default)
tk.Label(root, text="Significant Digits:").pack()
input_significant_digits = tk.Entry(root, width=30)
input_significant_digits.pack()
input_significant_digits.config(state="disabled")  # Disable input by default

# Enable/disable significant digits input based on selection
def toggle_significant_digits(*args):
    if shorten_digits_var.get() == "Yes":
        input_significant_digits.config(state="normal")
    else:
        input_significant_digits.delete(0, tk.END)
        input_significant_digits.config(state="disabled")

shorten_digits_var.trace("w", toggle_significant_digits)

# Checkbox for opening output.txt
open_output_var = tk.BooleanVar()
open_output_checkbox = tk.Checkbutton(root, text="Open output.txt after completion", variable=open_output_var)
open_output_checkbox.pack()

tk.Button(root, text="Run List Windows", command=execute_list_windows, width=20).pack(pady=10)

# Section: Open Windows
tk.Label(root, text="Open Windows", font=("Helvetica", 14)).pack(pady=10)
tk.Label(root, text="Filename:").pack()
input_filename = tk.Entry(root, width=30)
input_filename.pack()

tk.Label(root, text="Number of Windows:").pack()
input_num_windows = tk.Entry(root, width=30)
input_num_windows.insert(0, "5")  # Default value
input_num_windows.pack()

tk.Label(root, text="Viewer:").pack()
input_viewer = tk.Entry(root, width=30)
input_viewer.insert(0, "Notepad")  # Default viewer
input_viewer.pack()

tk.Button(root, text="Run Open Windows", command=execute_open_windows, width=20).pack(pady=10)

# Exit button
tk.Button(root, text="Exit", command=exit_program, width=10).pack(pady=20)

# Start the GUI event loop
update_working_dir()  # Initialize the directory display
root.mainloop()
