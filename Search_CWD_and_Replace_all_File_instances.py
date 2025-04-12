# Script Developer: Gabriel Mihai Sandu
# GitHub Profile: https://github.com/Gabrieliam42

import os
import sys
import ctypes
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception as e:
        print("Admin check failed:", e)
        return False

def run_as_admin():
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    if ret <= 32:
        print("Failed to elevate privileges.")
    sys.exit()

def search_and_replace(target_filename, replacement_file, search_directory):
    # First, gather all files matching the target filename
    matches = []
    for root, dirs, files in os.walk(search_directory):
        for file in files:
            if file == target_filename:
                target_path = os.path.join(root, file)
                matches.append(target_path)

    if not matches:
        messagebox.showinfo("Info", f"No files named '{target_filename}' were found in:\n{search_directory}")
        return

    # For each match, ask whether to replace it
    for target_path in matches:
        answer = messagebox.askquestion("Replace File",
                                        f"Do you want to replace this file?\n{target_path}")
        if answer == "yes":
            try:
                shutil.copy2(replacement_file, target_path)
                messagebox.showinfo("Success", f"Replaced file:\n{target_path}")
            except Exception as e:
                # Skip if the file is in use (or any other access error) and notify the user
                messagebox.showwarning("Warning",
                    f"Skipped replacing file (it may be in use or inaccessible):\n{target_path}\n\nError: {str(e)}")
        else:
            print("Skipped replacement for:", target_path)

def main():
    if not is_admin():
        print("Not running as administrator. Attempting to restart with admin privileges...")
        run_as_admin()

    # Initialize Tkinter and hide the root window.
    root = tk.Tk()
    root.withdraw()
    root.update()

    # Let the user choose the directory to search.
    search_directory = filedialog.askdirectory(title="Select Directory to Search", initialdir=os.getcwd())
    if not search_directory:
        search_directory = os.getcwd()

    # Ask the user for the target file name to search for.
    target_filename = simpledialog.askstring(
        "Target File",
        "Enter the target filename to search for (e.g., Register_Python310.exe):",
        initialvalue="Register_Python310.exe"
    )
    if not target_filename:
        messagebox.showerror("Error", "No target file name provided. Exiting.")
        sys.exit(1)

    # Ask the user to select the replacement file.
    replacement_file = filedialog.askopenfilename(
        title="Select Replacement File",
        initialdir="E:\\Scripts",
        filetypes=[("Executable Files", "*.exe"), ("All Files", "*.*")]
    )
    if not replacement_file:
        messagebox.showerror("Error", "No replacement file selected. Exiting.")
        sys.exit(1)

    # Confirm the replacement file exists.
    if not os.path.exists(replacement_file):
        messagebox.showerror("Error", f"Replacement file does not exist:\n{replacement_file}")
        sys.exit(1)

    messagebox.showinfo("Info", "Starting search and replace process...")
    search_and_replace(target_filename, replacement_file, search_directory)
    messagebox.showinfo("Done", "Process completed.")
    root.destroy()

if __name__ == "__main__":
    main()
