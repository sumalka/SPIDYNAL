@echo off
SETLOCAL EnableDelayedExpansion

:: Set console color (Green text on black background)
title SPIDYNAL Launcher

:START
cls
echo ==================================================
echo                    SPIDYNAL Setup       
echo ==================================================
echo.

:: Check if Python is installed
echo [CHECKING] Verifying Python installation...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [INFO] Python is not installed. Starting setup...
    echo.
    
    :: Download Python installer with timeout and error checking
    echo [DOWNLOADING] Fetching Python 3.12.2 installer...
    powershell -Command "& {try {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe' -OutFile 'python_installer.exe' -TimeoutSec 60} catch {Write-Output $_.Exception.Message > 'errorlog.txt'; exit 1}}" 2>nul
    IF !ERRORLEVEL! NEQ 0 (
        set /p ERRORMSG=<errorlog.txt 2>nul
        if "!ERRORMSG!"=="" set "ERRORMSG=Unknown error or timeout during download"
        echo [ERROR] Download failed: !ERRORMSG!
        :python_retry_prompt
        echo.
        set "CHOICE="
        <nul set /p "=Retry download? (y/n): "
        set /p CHOICE=""
        if /i "!CHOICE!"=="y" (
            cls
            echo [RETRYING] Fetching Python 3.12.2 installer...
            powershell -Command "& {try {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe' -OutFile 'python_installer.exe' -TimeoutSec 60} catch {Write-Output $_.Exception.Message > 'errorlog.txt'; exit 1}}" 2>nul
            IF !ERRORLEVEL! NEQ 0 (
                set /p ERRORMSG=<errorlog.txt 2>nul
                if "!ERRORMSG!"=="" set "ERRORMSG=Unknown error or timeout during download"
                echo [ERROR] Download failed again: !ERRORMSG!
                goto python_retry_prompt
            )
        ) else if /i "!CHOICE!"=="n" (
            echo [INFO] Canceling Python installation...
            del errorlog.txt 2>nul
            echo [EXIT] Setup aborted. Press any key to close...
            pause >nul
            exit /b 1
        ) else (
            echo [WARNING] Invalid input. Please enter 'y' or 'n'.
            goto python_retry_prompt
        )
    )
    del errorlog.txt 2>nul

    :: Install Python silently and add to PATH with error checking
    echo [INSTALLING] Setting up Python...
    python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
    IF %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Python installation failed with error code: %ERRORLEVEL%
        :install_retry_prompt
        echo.
        set "CHOICE="
        <nul set /p "=Retry installation? (y/n): "
        set /p CHOICE=""
        if /i "!CHOICE!"=="y" (
            cls
            echo [RETRYING] Setting up Python...
            python_installer.exe /quiet InstallAllUsers=1 PrependPath=1
            IF !ERRORLEVEL! NEQ 0 (
                echo [ERROR] Installation failed again with error code: !ERRORLEVEL!
                goto install_retry_prompt
            )
        ) else if /i "!CHOICE!"=="n" (
            echo [INFO] Canceling Python installation...
            del python_installer.exe 2>nul
            echo [EXIT] Setup aborted. Press any key to close...
            pause >nul
            exit /b 1
        ) else (
            echo [WARNING] Invalid input. Please enter 'y' or 'n'.
            goto install_retry_prompt
        )
    )
    
    :: Delete installer after installation
    del python_installer.exe 2>nul

    :: Refresh environment variables and verify Python installation
    echo [CONFIGURING] Updating system PATH...
    set "PATH=%PATH%;C:\Python312\Scripts;C:\Python312"
    setx PATH "%PATH%" >nul 2>&1
    python --version >nul 2>&1
    IF !ERRORLEVEL! NEQ 0 (
        echo [ERROR] Python installed but not detected in PATH.
        echo [INFO] Please restart your system or command prompt and try again.
        echo [EXIT] Press any key to close...
        pause >nul
        exit /b 1
    )
    
    echo [SUCCESS] Python installed successfully!
    echo [INFO] Restarting script in 2 seconds...
    timeout /t 2 /nobreak >nul
    start "" "%~f0"
    exit /b
)

:: Install required Python libraries with error checking
cls
echo ==================================================
echo          Checking on Python Libraries             
echo ==================================================
echo.

echo [UPDATING] Upgrading pip...
python -m pip install --upgrade pip 2>errorlog.txt
IF %ERRORLEVEL% NEQ 0 (
    set /p ERRORMSG=<errorlog.txt
    echo [ERROR] Failed to upgrade pip: !ERRORMSG!
    :pip_retry_prompt
    echo.
    set "CHOICE="
    <nul set /p "=Retry upgrading pip? (y/n): "
    set /p CHOICE=""
    if /i "!CHOICE!"=="y" (
        cls
        echo [RETRYING] Upgrading pip...
        python -m pip install --upgrade pip 2>errorlog.txt
        IF !ERRORLEVEL! NEQ 0 (
            set /p ERRORMSG=<errorlog.txt
            echo [ERROR] Failed again: !ERRORMSG!
            goto pip_retry_prompt
        )
    ) else if /i "!CHOICE!"=="n" (
        echo [INFO] Skipping pip upgrade...
    ) else (
        echo [WARNING] Invalid input. Please enter 'y' or 'n'.
        goto pip_retry_prompt
    )
)
del errorlog.txt 2>nul
echo [SUCCESS] pip updated.

:: Install psutil
echo [INSTALLING] psutil...
pip install psutil 2>errorlog.txt
IF %ERRORLEVEL% NEQ 0 (
    set /p ERRORMSG=<errorlog.txt
    echo [ERROR] Failed to install psutil: !ERRORMSG!
    :psutil_retry_prompt
    echo.
    set "CHOICE="
    <nul set /p "=Retry installing psutil? (y/n): "
    set /p CHOICE=""
    if /i "!CHOICE!"=="y" (
        cls
        echo [RETRYING] Installing psutil...
        pip install psutil 2>errorlog.txt
        IF !ERRORLEVEL! NEQ 0 (
            set /p ERRORMSG=<errorlog.txt
            echo [ERROR] Failed again: !ERRORMSG!
            goto psutil_retry_prompt
        )
    ) else if /i "!CHOICE!"=="n" (
        echo [INFO] Skipping psutil installation...
    ) else (
        echo [WARNING] Invalid input. Please enter 'y' or 'n'.
        goto psutil_retry_prompt
    )
)
del errorlog.txt 2>nul
echo [SUCCESS] psutil installed.

:: Install pygame
echo [INSTALLING] pygame...
pip install pygame 2>errorlog.txt
IF %ERRORLEVEL% NEQ 0 (
    set /p ERRORMSG=<errorlog.txt
    echo [ERROR] Failed to install pygame: !ERRORMSG!
    :pygame_retry_prompt
    echo.
    set "CHOICE="
    <nul set /p "=Retry installing pygame? (y/n): "
    set /p CHOICE=""
    if /i "!CHOICE!"=="y" (
        cls
        echo [RETRYING] Installing pygame...
        pip install pygame 2>errorlog.txt
        IF !ERRORLEVEL! NEQ 0 (
            set /p ERRORMSG=<errorlog.txt
            echo [ERROR] Failed again: !ERRORMSG!
            goto pygame_retry_prompt
        )
    ) else if /i "!CHOICE!"=="n" (
        echo [INFO] Skipping pygame installation...
    ) else (
        echo [WARNING] Invalid input. Please enter 'y' or 'n'.
        goto pygame_retry_prompt
    )
)
del errorlog.txt 2>nul
echo [SUCCESS] pygame installed.

:: Install colorama
echo [INSTALLING] colorama...
pip install colorama 2>errorlog.txt
IF %ERRORLEVEL% NEQ 0 (
    set /p ERRORMSG=<errorlog.txt
    echo [ERROR] Failed to install colorama: !ERRORMSG!
    :colorama_retry_prompt
    echo.
    set "CHOICE="
    <nul set /p "=Retry installing colorama? (y/n): "
    set /p CHOICE=""
    if /i "!CHOICE!"=="y" (
        cls
        echo [RETRYING] Installing colorama...
        pip install colorama 2>errorlog.txt
        IF !ERRORLEVEL! NEQ 0 (
            set /p ERRORMSG=<errorlog.txt
            echo [ERROR] Failed again: !ERRORMSG!
            goto colorama_retry_prompt
        )
    ) else if /i "!CHOICE!"=="n" (
        echo [INFO] Skipping colorama installation...
    ) else (
        echo [WARNING] Invalid input. Please enter 'y' or 'n'.
        goto colorama_retry_prompt
    )
)
del errorlog.txt 2>nul
echo [SUCCESS] colorama installed.

:: Install termcolor
echo [INSTALLING] termcolor...
pip install termcolor 2>errorlog.txt
IF %ERRORLEVEL% NEQ 0 (
    set /p ERRORMSG=<errorlog.txt
    echo [ERROR] Failed to install termcolor: !ERRORMSG!
    :termcolor_retry_prompt
    echo.
    set "CHOICE="
    <nul set /p "=Retry installing termcolor? (y/n): "
    set /p CHOICE=""
    if /i "!CHOICE!"=="y" (
        cls
        echo [RETRYING] Installing termcolor...
        pip install termcolor 2>errorlog.txt
        IF !ERRORLEVEL! NEQ 0 (
            set /p ERRORMSG=<errorlog.txt
            echo [ERROR] Failed again: !ERRORMSG!
            goto termcolor_retry_prompt
        )
    ) else if /i "!CHOICE!"=="n" (
        echo [INFO] Skipping termcolor installation...
    ) else (
        echo [WARNING] Invalid input. Please enter 'y' or 'n'.
        goto termcolor_retry_prompt
    )
)
del errorlog.txt 2>nul
echo [SUCCESS] termcolor installed.

:: Install speedtest-cli
echo [INSTALLING] speedtest-cli...
pip install speedtest-cli 2>errorlog.txt
IF %ERRORLEVEL% NEQ 0 (
    set /p ERRORMSG=<errorlog.txt
    echo [ERROR] Failed to install speedtest-cli: !ERRORMSG!
    :speedtest_retry_prompt
    echo.
    set "CHOICE="
    <nul set /p "=Retry installing speedtest-cli? (y/n): "
    set /p CHOICE=""
    if /i "!CHOICE!"=="y" (
        cls
        echo [RETRYING] Installing speedtest-cli...
        pip install speedtest-cli 2>errorlog.txt
        IF !ERRORLEVEL! NEQ 0 (
            set /p ERRORMSG=<errorlog.txt
            echo [ERROR] Failed again: !ERRORMSG!
            goto speedtest_retry_prompt
        )
    ) else if /i "!CHOICE!"=="n" (
        echo [INFO] Skipping speedtest-cli installation...
    ) else (
        echo [WARNING] Invalid input. Please enter 'y' or 'n'.
        goto speedtest_retry_prompt
    )
)
del errorlog.txt 2>nul
echo [SUCCESS] speedtest-cli installed.

:: Launch spidy.py in Windows Terminal maximized
cls
echo ==================================================
echo          Launching SPIDYNAL                       
echo ==================================================
echo.
echo [STARTING] Launching SPIDYNAL in Windows Terminal...
timeout /t 1 /nobreak >nul
wt -M python spidy.py
exit