@echo off
title TMS - Pasang Online (Mudah)
cd /d "%~dp0"
color 0E
echo.
echo  ====================================================
echo    TMS ONLINE - Banyak User + Update Realtime
echo  ====================================================
echo.
echo  Ikuti 3 langkah berurutan (copy-paste saja):
echo.
echo  ----------------------------------------------------
echo   LANGKAH 1 / 3 : Setup Database Supabase
echo  ----------------------------------------------------
echo   a) Notepad akan buka file supabase_setup.sql
echo   b) Browser akan buka SQL Editor Supabase
echo   c) COPY semua isi notepad ^> PASTE di SQL Editor
echo   d) Klik RUN (tombol hijau)
echo.
pause
start notepad "%~dp0supabase_setup.sql"
start https://supabase.com/dashboard/project/mezuatmcjqjxfsvepizv/sql/new
echo.
echo  Selesai langkah 1? Tekan tombol apa saja...
pause >nul
echo.
echo  ----------------------------------------------------
echo   LANGKAH 2 / 3 : Atur Kredensial Cloud
echo  ----------------------------------------------------
echo   Jalankan Atur_Cloud.bat untuk paste Anon Key.
echo.
set /p LANJUT="Jalankan Atur_Cloud sekarang? (Y/N): "
if /i "%LANJUT%"=="Y" call "%~dp0Atur_Cloud.bat"
echo.
echo  ----------------------------------------------------
echo   LANGKAH 3 / 3 : Pasang ke GitHub (akses online)
echo  ----------------------------------------------------
echo.
echo   Di GitHub, tambahkan 2 Secrets:
echo   Repo ^> Settings ^> Secrets and variables ^> Actions
echo.
echo   Nama secret 1 : SUPABASE_URL
echo   Isi           : https://mezuatmcjqjxfsvepizv.supabase.co
echo.
echo   Nama secret 2 : SUPABASE_ANON_KEY
echo   Isi           : (Anon Key yang sama dari Atur_Cloud)
echo.
echo   Lalu aktifkan Pages:
echo   Repo ^> Settings ^> Pages ^> Source: GitHub Actions
echo.
pause
start https://github.com/prasetiojayadwi-coder/tms-app/settings/secrets/actions
start https://github.com/prasetiojayadwi-coder/tms-app/settings/pages
echo.
echo  Setelah secrets + Pages aktif, push kode ke GitHub.
echo  URL aplikasi online:
echo   https://prasetiojayadwi-coder.github.io/tms-app/
echo.
echo  Bagikan URL itu ke semua user di tim Anda.
echo.
pause
