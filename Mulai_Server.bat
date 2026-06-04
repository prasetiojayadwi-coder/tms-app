@echo off
title TMS Local Server
echo Mencoba menjalankan server lokal untuk aplikasi TMS...
echo.

:: Cek Python
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo Python terdeteksi. Menjalankan server di http://localhost:8080 ...
    echo (Tekan Ctrl + C untuk menghentikan server)
    start http://localhost:8080/index.html
    python -m http.server 8080
    goto end
)

:: Cek Node/npx
where npx >nul 2>nul
if %errorlevel% equ 0 (
    echo Node.js/npx terdeteksi. Menjalankan server di http://localhost:8080 ...
    echo (Tekan Ctrl + C untuk menghentikan server)
    start http://localhost:8080/index.html
    npx http-server -p 8080
    goto end
)

echo ====================================================================
echo PERINGATAN: Python atau Node.js tidak ditemukan di sistem Anda!
echo ====================================================================
echo Aplikasi TMS membutuhkan server lokal agar penyimpanan (localStorage)
echo dapat bekerja secara permanen. Jika Anda membuka file index.html secara
echo langsung (double-click), data Anda tidak akan tersimpan setelah browser ditutup.
echo.
echo Rekomendasi Cara Menjalankan Server Lokal:
echo 1. Instal Python (https://www.python.org/downloads/)
echo    Lalu jalankan script ini kembali.
echo.
echo 2. Atau instal Node.js (https://nodejs.org/)
echo    Lalu jalankan script ini kembali.
echo.
echo 3. Atau gunakan ekstensi browser Chrome seperti "Web Server for Chrome"
echo    dan pilih folder proyek ini (f:\1. JAYA\TMS).
echo ====================================================================
pause

:end
