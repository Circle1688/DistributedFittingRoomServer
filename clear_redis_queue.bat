@echo off
cd /d "%~dp0"
cd Redis/
redis-cli.exe FLUSHALL
