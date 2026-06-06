@echo off
title TMS - Atur Cloud (Mudah)
cd /d "%~dp0"
echo.
echo  ============================================
echo    TMS - Atur Cloud Supabase (MUDAH)
echo  ============================================
echo.
echo  Hanya 2 langkah:
echo.
echo  [1] Browser akan terbuka ke halaman Supabase.
echo      Tab "Publishable and secret API keys"
echo      Copy key baris "api_tms" (sb_publishable_...)
echo.
echo  [2] Kembali ke jendela ini, PASTE key-nya.
echo.
pause
start https://supabase.com/dashboard/project/mezuatmcjqjxfsvepizv/settings/api-keys
echo.
python atur_cloud.py
if errorlevel 1 (
    echo.
    echo  Gagal menyimpan. Pastikan Python terinstall.
    pause
    exit /b 1
)
echo.
echo  ============================================
echo    SELESAI! config.js sudah tersimpan.
echo  ============================================
echo.
echo  Langkah terakhir: double-click Mulai_Server.bat
echo.
set /p JALANKAN="Jalankan server sekarang? (Y/N): "
if /i "%JALANKAN%"=="Y" (
    start "" "%~dp0Mulai_Server.bat"
)
pause
