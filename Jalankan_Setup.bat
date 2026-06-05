@echo off
title TMS - Setup Otomatis
cd /d "%~dp0"
echo.
python jalankan_setup.py
echo.
if errorlevel 2 (
    echo.
    echo  SQL belum dijalankan. Notepad + SQL Editor akan dibuka...
    start notepad "%~dp0supabase_setup.sql"
    start https://supabase.com/dashboard/project/mezuatmcjqjxfsvepizv/sql/new
)
pause
