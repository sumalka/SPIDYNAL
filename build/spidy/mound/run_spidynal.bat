@echo off
set COMMAND=%1
set QUERY=%2
set EXT=%3

if "%COMMAND%"=="net speed" (
    SPIDYNAL.exe net speed
) else if "%COMMAND%"=="spidy lens" (
    SPIDYNAL.exe spidy lens "%QUERY%" "%EXT%"
) else (
    echo Unsupported command: %COMMAND%
    exit /b 1
)