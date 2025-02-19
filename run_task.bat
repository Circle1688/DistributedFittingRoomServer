@echo off
title taskserver
cd /d "%~dp0"
set PYTHON=%~dp0.venv\Scripts\python.exe

%PYTHON% task_server.py

pause