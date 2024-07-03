import json
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, filedialog, Menu, Text
from ftplib import FTP
import os
import shutil

CONFIG_FILE = 'ftp_config.json'
LOCAL_FILE_PATH = 'phone_book.json'
REMOTE_FILE_PATH = '/data/phone_book.json'
BACKUP_FILE_PATH = 'phone_book_backup.json'
DATA_FOLDER = 'data'

# Embedding README content
README_CONTENT = """
# EZ Updater

## Overview

EZ Updater is a tool designed to manage a phone book JSON file via an FTP server. It provides a user-friendly interface for adding, deleting, and updating brands and models in the phone book. The tool also supports file uploads, where users can add new models and brands by uploading files directly.

## Features

- Add and delete brands and models.
- Upload files to automatically populate brand and model information.
- Save changes to the phone book and upload them to an FTP server.
- Read embedded README for instructions.

## Getting Started

### Initial Setup

1. **FTP Configuration**:
    - When you first run EZ Updater, you will be prompted to enter the FTP Host, Username, and Password.
    - You can choose to save these credentials for future use.

2. **Loading Data**:
    - The tool will download the current phone book JSON file from the FTP server.

### Main Interface

- **Brand Selection**:
    - Select an existing brand from the dropdown menu to manage its models.
- **Model Selection**:
    - Select an existing model from the dropdown menu to view or modify it.

### Adding and Deleting Entries

- **Add Brand**:
    - Click the "Add Brand" button and enter the new brand name.
- **Delete Brand**:
    - Select a brand from the dropdown and click the "Delete Brand" button.
- **Add Model**:
    - Select a brand, click the "Add Model" button, and enter the new model name, file, and suffix information.
- **Delete Model**:
    - Select a brand and model, then click the "Delete Model" button.

### Uploading Files

- Click the "Upload File" button to select a file from your computer.
- The tool will suggest a brand and model name based on the file name.
- Confirm or edit the suggested names, and the file will be added to the data folder and the phone book JSON will be updated.

### Saving Changes

- Click the "Save Changes" button to save any modifications to the phone book JSON and upload it to the FTP server.

## Help

- **Open README**:
    - Click on "Help" in the menu bar and select "Open README" to view this guide.

## Dependencies

- `tkinter`: Used for the GUI.
- `ftplib`: Used for FTP operations.
- `json`: Used for JSON file handling.
- `shutil`: Used for file operations.

## Compiling to an Executable

To compile this script into a standalone executable on Windows, follow these steps:

1. Install `pyinstaller`:
    ```sh
    pip install pyinstaller
    ```

2. Compile the script:
    ```sh
    pyinstaller --onefile --windowed EZUpdater.py
    ```

This command will create a single executable file in the `dist` directory.

## License

This project is licensed under the MIT License.
"""

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None

def prompt_for_credentials():
    dialog = tk.Toplevel()
    dialog.title("FTP Setup")

    tk.Label(dialog, text="Enter FTP Host:").grid(row=0, column=0)
    ftp_host = tk.Entry(dialog)
    ftp_host.grid(row=0, column=1)

    tk.Label(dialog, text="Enter FTP Username:").grid(row=1, column=0)
    ftp_user = tk.Entry(dialog)
    ftp_user.grid(row=1, column=1)

    tk.Label(dialog, text="Enter FTP Password:").grid(row=2, column=0)
    ftp_pass = tk.Entry(dialog, show='*')
    ftp_pass.grid(row=2, column=1)

    def save_credentials():
        config = {
            'FTP_HOST': ftp_host.get(),
            'FTP_USER': ftp_user.get(),
            'FTP_PASS': ftp_pass.get()
        }
        if messagebox.askyesno("Save Credentials", "Do you want to save these credentials?"):
            save_config(config)
        dialog.destroy()
        return config

    tk.Button(dialog, text="OK", command=save_credentials).grid(row=3, column=1)

    dialog.transient()
    dialog.grab_set()
    dialog.wait_window()

    return {
        'FTP_HOST': ftp_host.get(),
        'FTP_USER': ftp_user.get(),
        'FTP_PASS': ftp_pass.get()
    }

def download_file(ftp_host, ftp_user, ftp_pass, local_file_path, remote_file_path):
    ftp = FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)
    with open(local_file_path, 'wb') as f:
        ftp.retrbinary(f'RETR ' + remote_file_path, f.write)
    ftp.quit()

def upload_file_to_ftp(ftp_host, ftp_user, ftp_pass, local_path, remote_path):
    ftp = FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)
    with open(local_path, 'rb') as f:
        ftp.storbinary(f'STOR ' + remote_path, f)
    ftp.quit()

def create_backup():
    if os.path.exists(LOCAL_FILE_PATH):
        shutil.copy(LOCAL_FILE_PATH, BACKUP_FILE_PATH)
        messagebox.showinfo("Backup", "Backup created successfully.")

def load_json():
    with open(LOCAL_FILE_PATH, 'r') as f:
        return json.load(f)

def save_json(data):
    with open(LOCAL_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def update_entry(data, brand, model, new_file=None, new_suffix=None, delete=False):
    for entry in data:
        if entry['name'] == brand:
            if delete:
                entry['phones'] = [phone for phone in entry['phones'] if phone['name'] != model]
            else:
                for phone in entry['phones']:
                    if phone['name'] == model:
                        if new_file is not None:
                            phone['file'] = new_file
                        if new_suffix is not None:
                            phone['suffix'] = new_suffix
            break
    else:
        # Brand not found, add new brand
        data.append({'name': brand, 'phones': [{'name': model, 'file': new_file, 'suffix': new_suffix}]})

def sort_phone_book(data):
    # Sort the phone book by brand and then by model
    for entry in data:
        entry['phones'] = sorted(entry['phones'], key=lambda x: x['name'])
    data.sort(key=lambda x: x['name'])

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("EZ Updater")

        # Create and configure style
        style = ttk.Style()
        style.configure("TFrame", background="#333333")
        style.configure("TLabel", background="#333333", foreground="#ffffff", font=("Helvetica", 12))
        style.configure("TButton", background="#555555", foreground="#000000", font=("Helvetica", 10, "bold"), padding=10)
        style.map("TButton", background=[("active", "#777777")])

        self.config = load_config()
        if not self.config:
            self.config = prompt_for_credentials()

        self.download_phone_book()
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root, padding="10 10 10 10", style="TFrame")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Brand selection
        ttk.Label(self.frame, text="Select Brand:", style="TLabel").grid(row=0, column=0, sticky=tk.W)
        self.selected_brand = tk.StringVar()
        self.brand_menu = ttk.Combobox(self.frame, textvariable=self.selected_brand)
        self.brand_menu.grid(row=0, column=1, sticky=(tk.W, tk.E))
        self.brand_menu.bind('<<ComboboxSelected>>', self.load_models)

        # Model selection
        ttk.Label(self.frame, text="Select Model:", style="TLabel").grid(row=1, column=0, sticky=tk.W)
        self.selected_model = tk.StringVar()
        self.model_menu = ttk.Combobox(self.frame, textvariable=self.selected_model)
        self.model_menu.grid(row=1, column=1, sticky=(tk.W, tk.E))

        # Buttons
        self.button_frame = ttk.Frame(self.frame, padding="5 5 5 5", style="TFrame")
        self.button_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Button(self.button_frame, text="Add Brand", command=self.add_brand, style="TButton").grid(row=0, column=0, sticky=tk.W)
        ttk.Button(self.button_frame, text="Delete Brand", command=self.delete_brand, style="TButton").grid(row=0, column=1, sticky=tk.W)
        ttk.Button(self.button_frame, text="Add Model", command=self.add_model, style="TButton").grid(row=0, column=2, sticky=tk.W)
        ttk.Button(self.button_frame, text="Delete Model", command=self.delete_model, style="TButton").grid(row=0, column=3, sticky=tk.W)
        ttk.Button(self.button_frame, text="Save Changes", command=self.save_changes, style="TButton").grid(row=0, column=4, sticky=tk.W)
        ttk.Button(self.button_frame, text="Upload File", command=self.upload_file, style="TButton").grid(row=0, column=5, sticky=tk.W)
        ttk.Button(self.button_frame, text="Create Backup", command=create_backup, style="TButton").grid(row=0, column=6, sticky=tk.W)
        
        # Load initial data
        self.data = load_json()
        self.load_brands()

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Open README", command=self.open_readme)

    def open_readme(self):
        top = tk.Toplevel(self.root)
        top.title("README")

        text = Text(top, wrap='word', background="#333333", foreground="#ffffff", font=("Helvetica", 12))
        text.insert('1.0', README_CONTENT)
        text.config(state='disabled')  # Make the Text widget read-only
        text.pack(expand=1, fill='both')

    def download_phone_book(self):
        try:
            download_file(self.config['FTP_HOST'], self.config['FTP_USER'], self.config['FTP_PASS'], LOCAL_FILE_PATH, REMOTE_FILE_PATH)
            messagebox.showinfo("Download", "Phone book downloaded successfully.")
        except Exception as e:
            messagebox.showerror("Download Error", f"Failed to download phone book: {e}")

    def load_brands(self):
        self.brand_menu['values'] = sorted([entry['name'] for entry in self.data])

    def load_models(self, event):
        brand = self.selected_brand.get()
        for entry in self.data:
            if entry['name'] == brand:
                self.model_menu['values'] = sorted([phone['name'] for phone in entry['phones']])
                break

    def add_brand(self):
        new_brand = simpledialog.askstring("Add Brand", "Enter new brand name:")
        if new_brand:
            self.data.append({'name': new_brand, 'phones': []})
            self.brand_menu['values'] = sorted([entry['name'] for entry in self.data])

    def delete_brand(self):
        brand = self.selected_brand.get()
        self.data = [entry for entry in self.data if entry['name'] != brand]
        self.load_brands()
        self.model_menu['values'] = []

    def add_model(self):
        brand = self.selected_brand.get()
        new_model = simpledialog.askstring("Add Model", "Enter new model name:")
        if new_model:
            new_file = simpledialog.askstring("Add Model file", "Enter new model file (comma-separated):")
            new_suffix = simpledialog.askstring("Add Model suffix", "Enter new model suffix (comma-separated):")
            new_file_list = [file.strip() for file in new_file.split(',')] if new_file else []
            new_suffix_list = [suffix.strip() for suffix in new_suffix.split(',')] if new_suffix else []
            for entry in self.data:
                if entry['name'] == brand:
                    entry['phones'].append({'name': new_model, 'file': new_file_list, 'suffix': new_suffix_list})
                    entry['phones'] = sorted(entry['phones'], key=lambda x: x['name'])
                    self.model_menu['values'] = [phone['name'] for phone in entry['phones']]
                    break

    def delete_model(self):
        brand = self.selected_brand.get()
        model = self.selected_model.get()
        update_entry(self.data, brand, model, delete=True)
        self.load_models(None)

    def save_changes(self):
        sort_phone_book(self.data)  # Sort the phone book before saving
        save_json(self.data)
        upload_file_to_ftp(self.config['FTP_HOST'], self.config['FTP_USER'], self.config['FTP_PASS'], LOCAL_FILE_PATH, REMOTE_FILE_PATH)
        messagebox.showinfo("Save Changes", "Changes saved and uploaded successfully!")

    def upload_file(self):
        # Select the file to upload
        file_path = filedialog.askopenfilename(title="Select a File")
        if not file_path:
            return

        # Suggest brand and model based on file name
        file_name = os.path.basename(file_path)
        suggested_brand, suggested_model = self.parse_file_name(file_name)

        # Ask user to confirm or edit the brand and model
        brand = simpledialog.askstring("Confirm Brand", "Enter or confirm brand:", initialvalue=suggested_brand)
        model = simpledialog.askstring("Confirm Model", "Enter or confirm model:", initialvalue=suggested_model)
        
        if brand and model:
            # Upload the file to the FTP server
            remote_file_path = f'/data/{file_name}'
            upload_file_to_ftp(self.config['FTP_HOST'], self.config['FTP_USER'], self.config['FTP_PASS'], file_path, remote_file_path)
            
            # Update the phone book data
            new_file_list = [file_name]
            update_entry(self.data, brand, model, new_file=new_file_list, new_suffix=[])
            self.load_brands()
            self.save_changes()

    def parse_file_name(self, file_name):
        # Simple parsing logic: split by underscores or dashes and use the first part as brand and second as model
        parts = os.path.splitext(file_name)[0].split('_')
        if len(parts) < 2:
            parts = os.path.splitext(file_name)[0].split('-')
        if len(parts) >= 2:
            return parts[0], parts[1]
        return "Unknown Brand", "Unknown Model"

# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
