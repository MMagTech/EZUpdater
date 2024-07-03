# EZ Updater

## Overview

EZ Updater is a tool designed to manage a phone book JSON file via an FTP server. It provides a user-friendly interface for adding, deleting, and updating brands and models in the phone book. The tool also supports file uploads, where users can add new models and brands by uploading files directly.

## Features

- Add and delete brands and models.
- Upload files to automatically populate brand and model information.
- Save changes to the phone book and upload them to an FTP server.
- Embedded README for instructions.

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

- Click the "Upload Files" button to select files from your computer.
- The tool will ensure you select exactly two files, one ending with 'L' and the other with 'R'.
- The tool will suggest a brand and model name based on the file names.
- Confirm or edit the suggested names, and the files will be uploaded to the FTP server with their original names.
- The phone book JSON will be updated with a single entry for the model without the 'L' or 'R' and without the file extension.

### Saving Changes

- Click the "Save Changes" button to save any modifications to the phone book JSON and upload it to the FTP server.

### Creating Backups

- Click the "Create Backup" button to create a backup of the current phone book JSON file.

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

file_path = "/mnt/data/README.md"
with open(file_path, "w") as file:
    file.write(readme_content)

file_path
