
# The Sims Resource Downloader  

[![Code Style: Black](https://img.shields.io/badge/Code_Style-Black-black.svg?style=for-the-badge)](https://github.com/psf/black) [![License: MIT](https://img.shields.io/github/license/Xientraa/The-Sims-Resource-Downloader?label=License&style=for-the-badge)](./LICENSE)  

I created this tool because I found it infuriating to download stuff from The Sims Resource, their 15-second wait along with only being able to download a single item at a time and them plastering advertisements everywhere for their VIP service.  

With this tool, you can download multiple items at once. Just copy the URL of the item, and the tool will monitor your clipboard for valid URLs. It will automatically start downloading the item to the directory specified in `config.json`.  

For a fully in-depth guide on how to set up and use this tool, check out the [Wiki](https://github.com/Xientraa/The-Sims-Resource-Downloader/wiki).  

## Configuration  

| Option | Description | Type |  
| - | - | - |  
| downloadDirectory | Path to a directory where the files will be downloaded to. | string |  
| maxActiveDownloads | Limits the number of concurrent downloads. | integer |  
| saveDownloadQueue | Toggles saving & loading of active and queued downloads. | boolean |  
| debug | Toggles debug messages from the logger. | boolean |  

## **Before Using, Make Sure Python is Installed!**  

This tool **requires Python** to run. If you have no clue what Python is, don’t worry. **You don’t need to know how to code**, just make sure Python is installed on your system.  

**Check if Python is already installed:**  
Open **Command Prompt (CMD)** or **PowerShell**, then type:  

```sh
python --version
```

If it shows a Python version, you’re good to go.  
If you get an error or it says Python isn’t recognized, **you need to install Python first!**  

### **How to Install Python (Windows):**  

#### **Option 1: The Easiest Way (via Winget)**  
Open **CMD or PowerShell**, then run:  

```sh
winget install Python.Python.3
```

#### **Option 2: Alternative (via PowerShell directly)**  
If `winget` isn’t available, you can install Python manually using PowerShell:  

```sh
Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe" -OutFile "python-installer.exe"; Start-Process "python-installer.exe" -Wait; Remove-Item "python-installer.exe"
```

After installing, **restart your terminal** and check again with `python --version`. If it shows a version number, you’re all set.  

## **Downloading This Repository**  

You can get this tool in two ways:  

#### **Option 1: Using Git (Recommended)**  
Open **CMD or PowerShell**, then run:  

```sh
git clone https://github.com/Xientraa/The-Sims-Resource-Downloader.git
cd The-Sims-Resource-Downloader
```

#### **Option 2: Downloading Manually**  
1. Go to [this link](https://github.com/Xientraa/The-Sims-Resource-Downloader).  
2. Click the green "Code" button, then select **Download ZIP**.  
3. Extract the ZIP file anywhere on your computer.  
4. Open **CMD or PowerShell**, then navigate to the extracted folder using `cd`.  

## **Setting Up Environment**  

Open **CMD or PowerShell**, make sure you're inside the project folder, then run:  

```sh
python -m venv ./env/
```

## **Installing Requirements**  

```sh
pip install -r requirements.txt
```

## **Usage**  

```sh
python src/main.py
```  



Now there’s **no excuse** for “why isn’t it working?”. Just **install Python first**, download the repo, and run the script!

