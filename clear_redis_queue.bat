@echo off
cd /d "%~dp0"
cd Redis/
redis-cli.exe FLUSHALL

if %errorlevel% equ 0 (
    echo FLUSHALL command executed successfully.
) else (
    echo Failed to execute FLUSHALL command.
)
pause