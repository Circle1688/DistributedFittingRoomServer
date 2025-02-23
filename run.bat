@echo off
title fittingroomserver
cd /d "%~dp0"

REM Start redis
start %~dp0run_redis.bat

REM Start task server
start %~dp0run_task.bat

REM Clear redis queue
start %~dp0clear_redis_queue.bat

REM Start fitting room server
set PYTHON=%~dp0.venv\Scripts\python.exe

%PYTHON% server.py

pause
