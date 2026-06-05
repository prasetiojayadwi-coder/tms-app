@echo off
title TMS - Selesaikan Setup Online
cd /d "%~dp0"
echo.
echo  ============================================
echo    TMS - Selesaikan Setup Online
echo  ============================================
echo.
echo  [1] Cek apakah SQL Supabase sudah dijalankan...
echo      Jika BELUM, Notepad + SQL Editor akan dibuka.
echo.
set /p SQLDONE="Sudah RUN supabase_setup.sql di Supabase? (Y/N): "
if /i not "%SQLDONE%"=="Y" (
    start notepad "%~dp0supabase_setup.sql"
    start https://supabase.com/dashboard/project/mezuatmcjqjxfsvepizv/sql/new
    echo.
    echo  Copy semua SQL ^> Paste ^> Run, lalu jalankan script ini lagi.
    pause
    exit /b 0
)
echo.
echo  [2] Push config online ke GitHub...
set GIT="C:\Program Files\Git\cmd\git.exe"
if not exist %GIT% (
    echo  Git tidak ditemukan. Install Git for Windows dulu.
    pause
    exit /b 1
)
%GIT% add config.deploy.js .github/workflows/deploy-pages.yml .gitignore atur_cloud.py 2>nul
%GIT% diff --cached --quiet
if %errorlevel% equ 0 (
    echo  Tidak ada perubahan deploy. Memicu deploy ulang...
    %GIT% commit --allow-empty -m "Trigger redeploy TMS online"
) else (
    %GIT% commit -m "Perbaiki deploy online: config.deploy.js untuk cloud sync"
)
%GIT% push origin main
echo.
echo  [3] Tunggu 1-2 menit, lalu buka:
echo   https://prasetiojayadwi-coder.github.io/tms-app/
echo.
echo  Login ^> badge harus "Cloud Live" (hijau).
echo.
start https://github.com/prasetiojayadwi-coder/tms-app/actions
start https://prasetiojayadwi-coder.github.io/tms-app/
pause
