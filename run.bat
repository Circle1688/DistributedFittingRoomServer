@echo off
title FittingRoomServer
cd /d "%~dp0"
set PYTHON=%~dp0.venv\Scripts\python.exe

%PYTHON% server.py

pause
