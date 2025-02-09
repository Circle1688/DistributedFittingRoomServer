@echo off
set CELERY=%~dp0.venv\Scripts\celery.exe

start "" http://localhost:5555/

%CELERY% -A faceswap flower

pause