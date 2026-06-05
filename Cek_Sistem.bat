@echo off
title TMS - Cek Kesehatan Sistem
cd /d "%~dp0"
echo.
echo ========================================
echo   TMS - Pemeriksaan Kesehatan Sistem
echo ========================================
echo.
echo Pastikan server sudah berjalan (Mulai_Server.bat)
echo di http://localhost:8080 sebelum menjalankan cek ini.
echo.
python cek_sistem.py
echo.
pause
