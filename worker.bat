@echo off
set CELERY=%~dp0.venv\Scripts\celery.exe

%CELERY% -A faceswap worker -P gevent -Q high_priority,low_priority -l INFO --concurrency=1
