## Screenshot Copier (Windows)

This is the Windows version of Screenshot Copier.
There is also a macOS version available.
The purpose of the application is simple:
When you take a screenshot on one device, the app automatically sends it to your second device's clipboard.
You must install this application on both devices.
One device will act as the Sender
The other device will act as the Receiver
When the sender takes a screenshot, it will automatically be transferred to the receiver’s clipboard.
Both devices can be:
Windows
macOS
It does not matter — just make sure you download the correct repository version for your operating system.

## System Requirements
Windows 10 / 11
Python 3.9+
Git
bash (can use git bash)
pip

## Install Git (if not installed)
Check:
```bash
git --version
```
If Git is not installed, download it from:
https://git-scm.com
Install it and make sure "Add Git to PATH" is enabled during setup.
## Clone the Repository
Open CMD or PowerShell:
```bash
git clone https://github.com/MertDikdas/screenshot-copier-windows.git
cd screenshot-copier-windows
```
## Install Dependencies
Create a virtual environment (recommended):
```bash
python -m venv .venv
.venv\Scripts\activate
```
## Install requirements:
```bash
pip install -r requirements.txt
```
## Run in Development Mode
```bash
python -m src.main
```
## Build Standalone .exe
Install PyInstaller:
```bash
pip install pyinstaller
```
Build executable:
```bash
pyinstaller --onefile src/main.py --name ScreenshotCopier --paths .
```
Output will be located in:
dist\ScreenshotCopier.exe
Run it:
```bash
cd dist
ScreenshotCopier.exe
```
You can move dist\ScreenshotCopier.exe anywhere you want.
