import json
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from ftplib import FTP
import os
import shutil

CONFIG_FILE = 'ftp_config.json'
LOCAL_FILE_PATH = 'phone_book.json'
REMOTE_FILE_PATH = '/data/phone_book.json'
BACKUP_FILE_PATH = 'phone_book_backup.json'

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None

def prompt_for_credentials():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    ftp_host = simpledialog.askstring("FTP Setup", "Enter FTP Host:")
    ftp_user = simpledialog.askstring("FTP Setup", "Enter FTP Username:")
    ftp_pass = simpledialog.askstring("FTP Setup", "Enter FTP Password:", show='*')
    save_credentials = messagebox.askyesno("Save Credentials", "Do you want to save these credentials?")
    
    config = {
        'FTP_HOST': ftp_host,
        'FTP_USER': ftp_user,
        'FTP_PASS': ftp_pass
    }
    
    if save_credentials:
        save_config(config)
    
    return config

def download_file(ftp_host, ftp_user, ftp_pass):
    ftp = FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)
    with open(LOCAL_FILE_PATH, 'wb') as f:
        ftp.retrbinary(f'RETR ' + REMOTE_FILE_PATH, f.write)
    ftp.quit()

def upload_file(ftp_host, ftp_user, ftp_pass):
    ftp = FTP(ftp_host)
    ftp.login(ftp_user, ftp_pass)
    with open(LOCAL_FILE_PATH, 'rb') as f:
        ftp.storbinary(f'STOR ' + REMOTE_FILE_PATH, f)
    ftp.quit()

def load_json():
    with open(LOCAL_FILE_PATH, 'r') as f:
        return json.load(f)

def save_json(data):
    with open(LOCAL_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)

def update_entry(data, brand, model, new_files=None, new_suffixes=None, delete=False):
    for entry in data:
        if entry['name'] == brand:
            if delete:
                entry['phones'] = [phone for phone in entry['phones'] if phone['name'] != model]
            else:
                for phone in entry['phones']:
                    if phone['name'] == model:
                        if new_files:
                            phone['files'] = new_files
                        if new_suffixes:
                            phone['suffixes'] = new_suffixes
            return
    if not delete and new_files and new_suffixes:
        data.append({'name': brand, 'phones': [{'name': model, 'files': new_files, 'suffixes': new_suffixes}]})

def create_backup():
    shutil.copyfile(LOCAL_FILE_PATH, BACKUP_FILE_PATH)

# Initialize GUI
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Phone Book Manager")
        self.config = load_config() or prompt_for_credentials()
        
        download_file(self.config['FTP_HOST'], self.config['FTP_USER'], self.config['FTP_PASS'])
        self.data = load_json()
        self.selected_brand = tk.StringVar()
        self.selected_model = tk.StringVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Brand selection
        tk.Label(self.root, text="Select Brand:").grid(row=0, column=0, padx=10, pady=5)
        self.brand_menu = ttk.Combobox(self.root, textvariable=self.selected_brand)
        self.brand_menu['values'] = sorted([entry['name'] for entry in self.data])
        self.brand_menu.grid(row=0, column=1, padx=10, pady=5)
        self.brand_menu.bind("<<ComboboxSelected>>", self.load_models)
        
        # Model selection
        tk.Label(self.root, text="Select Model:").grid(row=1, column=0, padx=10, pady=5)
        self.model_menu = ttk.Combobox(self.root, textvariable=self.selected_model)
        self.model_menu.grid(row=1, column=1, padx=10, pady=5)
        
        # Add/Delete Buttons
        tk.Button(self.root, text="Add Brand", command=self.add_brand).grid(row=2, column=0, padx=10, pady=5)
        tk.Button(self.root, text="Delete Brand", command=self.delete_brand).grid(row=2, column=1, padx=10, pady=5)
        tk.Button(self.root, text="Add Model", command=self.add_model).grid(row=3, column=0, padx=10, pady=5)
        tk.Button(self.root, text="Delete Model", command=self.delete_model).grid(row=3, column=1, padx=10, pady=5)
        
        # Backup and Save Buttons
        tk.Button(self.root, text="Create Backup", command=create_backup).grid(row=4, column=0, padx=10, pady=5)
        tk.Button(self.root, text="Save Changes", command=self.save_changes).grid(row=4, column=1, padx=10, pady=5)
    
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
            self.data = sorted(self.data, key=lambda x: x['name'])
            self.brand_menu['values'] = [entry['name'] for entry in self.data]
    
    def delete_brand(self):
        brand = self.selected_brand.get()
        self.data = [entry for entry in self.data if entry['name'] != brand]
        self.brand_menu['values'] = sorted([entry['name'] for entry in self.data])
        self.model_menu['values'] = []
    
    def add_model(self):
        brand = self.selected_brand.get()
        new_model = simpledialog.askstring("Add Model", "Enter new model name:")
        if new_model:
            new_files = simpledialog.askstring("Add Model Files", "Enter new model files (comma-separated):")
            new_suffixes = simpledialog.askstring("Add Model Suffixes", "Enter new model suffixes (comma-separated):")
            new_files_list = [file.strip() for file in new_files.split(',')] if new_files else []
            new_suffixes_list = [suffix.strip() for suffix in new_suffixes.split(',')] if new_suffixes else []
            for entry in self.data:
                if entry['name'] == brand:
                    entry['phones'].append({'name': new_model, 'files': new_files_list, 'suffixes': new_suffixes_list})
                    entry['phones'] = sorted(entry['phones'], key=lambda x: x['name'])
                    self.model_menu['values'] = [phone['name'] for phone in entry['phones']]
                    break
    
    def delete_model(self):
        brand = self.selected_brand.get()
        model = self.selected_model.get()
        update_entry(self.data, brand, model, delete=True)
        self.load_models(None)
    
    def save_changes(self):
        save_json(self.data)
        upload_file(self.config['FTP_HOST'], self.config['FTP_USER'], self.config['FTP_PASS'])
        messagebox.showinfo("Save Changes", "Changes saved and uploaded successfully!")

# Main entry point
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
