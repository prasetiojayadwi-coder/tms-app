@echo off
title TMS - Setup Konfigurasi Cloud
cd /d "%~dp0"

if exist config.js (
    echo config.js sudah ada. Tidak ada perubahan.
    goto end
)

if not exist config.example.js (
    echo ERROR: config.example.js tidak ditemukan!
    goto end
)

copy config.example.js config.js >nul
echo.
echo ========================================
echo   config.js berhasil dibuat!
echo ========================================
echo.
echo Silakan edit config.js dan isi:
echo   - supabase.url
echo   - supabase.anonKey
echo.
echo Dapatkan nilai tersebut dari:
echo   Supabase Dashboard ^> Project Settings ^> API
echo.

:end
pause
