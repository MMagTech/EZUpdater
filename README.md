# Phone Book Manager

Phone Book Manager is a Python-based GUI application for managing a phone book stored on an FTP server. The application allows you to download the phone book, make modifications, create backups, and upload the changes back to the server.

## Features

- **Download Phone Book**: Fetch the phone book data from an FTP server.
- **View and Select Brands and Models**: Browse through brands and models in the phone book.
- **Add and Delete Brands and Models**: Easily add or delete brands and models.
- **Create Backup**: Create a backup of the phone book before making changes.
- **Save Changes**: Save the modified phone book and upload it to the FTP server.
- **Alphabetical Order**: Ensure brands and models are displayed in alphabetical order.

## Requirements

- Python 3.x
- `tkinter` for the GUI (part of the standard library)
- `ftplib` for FTP operations (part of the standard library)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/MMagTech/EZUpdater.git
    cd EZUpdater
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:
    ```bash
    python EZUpdater.py
    ```

2. **FTP Configuration**: On the first run, you will be prompted to enter your FTP host, username, and password. You have the option to save these credentials for future use.

3. **Main Interface**:
    - **Select Brand**: Choose a brand from the drop-down menu to view its models.
    - **Select Model**: Choose a model from the drop-down menu to view or modify it.
    - **Add Brand**: Click the "Add Brand" button to add a new brand.
    - **Delete Brand**: Click the "Delete Brand" button to remove the selected brand.
    - **Add Model**: Click the "Add Model" button to add a new model to the selected brand. You will be prompted to enter the model name, files, and suffixes.
    - **Delete Model**: Click the "Delete Model" button to remove the selected model.
    - **Create Backup**: Click the "Create Backup" button to create a backup of the phone book.
    - **Save Changes**: Click the "Save Changes" button to save the modifications and upload them to the FTP server.

## Compiling to an Executable on Win
