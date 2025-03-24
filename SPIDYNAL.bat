@echo off
SETLOCAL

:: Check if Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Downloading and installing Python...
    
    :: Download Python installer
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe' -OutFile 'python_installer.exe'}"
    
    :: Install Python silently and add to PATH
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    
    :: Delete installer after installation
    del python_installer.exe

    :: Refresh environment variables
    setx PATH "%PATH%;C:\Python312\Scripts;C:\Python312"
    
    echo Python installed successfully. Restarting the script...
    start "" "%~f0"
    exit /b
)

:: Install required Python libraries
echo Installing required Python libraries...
python -m pip install --upgrade pip
pip install pygame colorama termcolor

:: Run your Python script
echo Running Spidy...
python build/spidy/mound/spidy.py
