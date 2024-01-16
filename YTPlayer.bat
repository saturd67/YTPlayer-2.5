@echo off

set "VENV_PATH=^"%CD%\venv\Scripts\activate.bat^""
call %VENV_PATH%
set "Main_PATH=^"%CD%\main.py^""
python %Main_PATH%

pause