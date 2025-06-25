@echo off

cd /D "%~dp0"

python --version > NUL
IF %ERRORLEVEL% NEQ 0 (
    ECHO Python is not installed, please install python and try again. https://www.python.org/downloads/
    @pause
    EXIT
)

IF NOT EXIST env (
    ECHO Python environment doesn't exist, creating python environment.
    python -m venv env
)

env\Scripts\pip.exe install -qr requirements.txt
env\Scripts\python.exe src\main.py
