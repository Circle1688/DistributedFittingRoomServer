@echo off
title worker
cd /d "%~dp0"
set CELERY=%~dp0.venv\Scripts\celery.exe

%CELERY% -A faceswap worker -P gevent -l INFO -O fair
