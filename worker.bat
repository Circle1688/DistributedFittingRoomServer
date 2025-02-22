@echo off
title worker
cd /d "%~dp0"
set CELERY=%~dp0.venv\Scripts\celery.exe

rem %CELERY% -A faceswap worker -P gevent -Q high_priority,low_priority -l INFO --concurrency=1
%CELERY% -A faceswap worker -P gevent -l INFO
