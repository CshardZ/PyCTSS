@echo off
setlocal

:: Path to Desktop
set "DESKTOP=%USERPROFILE%\Desktop"

:: Name + location of venv
set "VENV_DIR=%DESKTOP%\myenv"

echo Creating virtual environment at: %VENV_DIR%
python -m venv "%VENV_DIR%"

echo.
echo Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

echo.
echo Installing dependencies...
pip install rich prompt_toolkit

echo.
echo Running main.py...
python "%~dp0main.py"

echo.
echo All done. If something breaks, blame the electrons.
