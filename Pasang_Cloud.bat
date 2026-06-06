@echo off
title TMS - Pasang Cloud Key
cd /d "%~dp0"
color 0A
echo.
echo  ====================================================
echo    TMS - Pasang Publishable Key (api_tms)
echo  ====================================================
echo.
echo  [1] Browser akan buka halaman API Keys Supabase.
echo      Copy key dari baris "api_tms" (sb_publishable_...)
echo.
echo  [2] Kembali ke jendela ini, PASTE key, tekan Enter.
echo.
pause
start https://supabase.com/dashboard/project/mezuatmcjqjxfsvepizv/settings/api-keys
echo.
python pasang_key.py
echo.
if errorlevel 1 (
    echo  Gagal. Pastikan Python terinstall dan key benar.
    pause
    exit /b 1
)
echo.
start https://prasetiojayadwi-coder.github.io/tms-app/
pause
