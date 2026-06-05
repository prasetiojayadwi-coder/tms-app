#!/usr/bin/env python3
"""Pemeriksaan kesehatan TMS — jalankan tanpa browser."""
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PORT = 8080
BASE = f'http://localhost:{PORT}'
PASS = 0
FAIL = 0
WARN = 0


def ok(msg):
    global PASS
    PASS += 1
    print(f'  [OK]   {msg}')


def bad(msg):
    global FAIL
    FAIL += 1
    print(f'  [FAIL] {msg}')


def warn(msg):
    global WARN
    WARN += 1
    print(f'  [WARN] {msg}')


def fetch(path, timeout=8):
    return urllib.request.urlopen(f'{BASE}{path}', timeout=timeout)


def check_files():
    print('\n== File Proyek ==')
    required = ['index.html', 'manifest.json', 'sw.js', 'tms_pwa_icon.png', 'Mulai_Server.bat', 'config.example.js']
    for name in required:
        p = ROOT / name
        if p.exists() and p.stat().st_size > 0:
            ok(f'{name} ({p.stat().st_size:,} bytes)')
        else:
            bad(f'{name} tidak ditemukan atau kosong')

    cfg = ROOT / 'config.js'
    example = ROOT / 'config.example.js'
    if cfg.exists():
        text = cfg.read_text(encoding='utf-8')
        if 'YOUR-PROJECT' in text or 'YOUR_SUPABASE_ANON_KEY' in text:
            warn('config.js masih berisi placeholder — isi kredensial Supabase')
        elif 'supabase.co' in text and 'anonKey' in text:
            ok('config.js terkonfigurasi')
        else:
            warn('config.js ada tetapi format tidak dikenali')
    elif example.exists():
        warn('config.js belum ada — jalankan Setup_Config.bat lalu isi kredensial')
    else:
        bad('config.example.js hilang, tidak bisa setup cloud sync')


def check_html_integrity():
    print('\n== Integritas Kode HTML/JS ==')
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    scripts = [
        m.group(1) for m in re.finditer(r'<script(?:\s[^>]*)?>([\s\S]*?)</script>', html, re.I)
        if not m.group(1).strip().startswith('tailwind.config')
    ]
    js = '\n'.join(scripts)
    func_defs = set(re.findall(r'function\s+([a-zA-Z_$][\w$]*)\s*\(', js))

    onclick_calls = set()
    for m in re.finditer(r'onclick="([^"]+)"', html):
        cm = re.match(r'^([a-zA-Z_$][\w$]*)\s*\(', m.group(1))
        if cm:
            onclick_calls.add(cm.group(1))
    missing_onclick = sorted(onclick_calls - func_defs)
    if missing_onclick:
        bad(f'Handler onclick tanpa fungsi: {", ".join(missing_onclick)}')
    else:
        ok(f'Semua {len(onclick_calls)} handler onclick valid')

    onsubmit_ok = True
    for m in re.finditer(r'onsubmit="([^"]+)"', html):
        cm = re.match(r'^([a-zA-Z_$][\w$]*)\s*\(', m.group(1))
        if cm and cm.group(1) not in func_defs:
            bad(f'Handler onsubmit tanpa fungsi: {cm.group(1)}')
            onsubmit_ok = False
    if onsubmit_ok:
        ok('Semua handler onsubmit valid')

    tabs = set(re.findall(r"switchTab\('([^']+)'\)", html))
    views = set(re.findall(r'id="view-([^"]+)"', html))
    missing_views = sorted(tabs - views)
    if missing_views:
        bad(f'Tab tanpa view: {", ".join(missing_views)}')
    else:
        ok(f'Semua {len(tabs)} tab navigasi punya view')

    if 'initHandoverCanvas' in js:
        warn('Kode legacy initHandoverCanvas masih ada')
    else:
        ok('Kode legacy handover canvas sudah dibersihkan')

    for cid in ['sig-canvas', 'handover-sig-canvas-giver', 'handover-sig-canvas-receiver']:
        if cid in html:
            ok(f'Canvas {cid} ada')
        else:
            bad(f'Canvas {cid} hilang')

    if 'bg-red-650' in html:
        warn('Class CSS tidak valid: bg-red-650')
    if 'border-gray-150' in html:
        warn('Class CSS tidak valid: border-gray-150')
    if 'border-lux-850' in html:
        warn('Class CSS tidak valid: border-lux-850')

    if 'mezuatmcjqjxfsvepizv' in html or 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' in html:
        bad('Kredensial Supabase masih tertanam di index.html')
    elif 'config.js' in html:
        ok('Kredensial Supabase dipisah ke config.js')
    else:
        warn('config.js tidak direferensikan di index.html')


def check_server():
    print('\n== Server Lokal ==')
    try:
        r = fetch('/index.html')
        body = r.read()
        if r.status == 200 and len(body) > 100_000:
            ok(f'index.html dilayani ({len(body):,} bytes)')
        else:
            bad(f'index.html tidak normal (status {r.status})')
    except urllib.error.URLError:
        bad(f'Server tidak berjalan di {BASE}')
        warn('Jalankan Mulai_Server.bat terlebih dahulu, lalu ulangi cek ini')
        return

    for path in ['config.js', 'manifest.json', 'sw.js', 'tms_pwa_icon.png']:
        try:
            r = fetch('/' + path)
            r.read()
            ok(f'{path} HTTP {r.status}')
        except Exception as e:
            bad(f'{path}: {e}')


def check_git():
    print('\n== Git / GitHub ==')
    git = r'C:\Program Files\Git\cmd\git.exe'
    if not Path(git).exists():
        warn('Git tidak ditemukan — lewati pemeriksaan GitHub')
        return

    def git_run(*args):
        r = subprocess.run([git, *args], cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
        return r.stdout.strip(), r.returncode

    remote, _ = git_run('remote', 'get-url', 'origin')
    if remote:
        ok(f'Remote: {remote}')
    else:
        bad('Remote origin tidak dikonfigurasi')
        return

    tracked, _ = git_run('ls-files')
    tracked_set = set(tracked.splitlines()) if tracked else set()
    if 'config.js' in tracked_set:
        bad('KRITIS: config.js ter-track di git — kredensial bisa bocor ke GitHub')
    else:
        ok('config.js tidak ter-track')

    _, ignore_code = git_run('check-ignore', '-v', 'config.js')
    if ignore_code == 0:
        ok('.gitignore melindungi config.js')
    elif Path('.gitignore').exists():
        warn('.gitignore ada tetapi config.js belum ter-ignore')

    if 'config.example.js' not in tracked_set:
        warn('config.example.js belum di-commit ke GitHub')

    status, _ = git_run('status', '-sb')
    if any(line.startswith('??') for line in status.splitlines()[1:]):
        warn('Ada file baru yang belum di-commit')
    if ' M ' in f' {status} ' or '\n M ' in status:
        warn('Ada perubahan lokal yang belum di-commit')

    remote_html, rc = git_run('show', 'origin/main:index.html')
    if rc == 0:
        if 'mezuatmcjqjxfsvepizv' in remote_html or 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9' in remote_html:
            bad('KRITIS: GitHub origin/main masih memuat kredensial di index.html — perlu push perbaikan')
        else:
            ok('GitHub origin/main bebas kredensial hardcoded')


def main():
    print('========================================')
    print('  TMS — Pemeriksaan Kesehatan Sistem')
    print('========================================')
    check_files()
    check_html_integrity()
    check_git()
    check_server()
    print('\n========================================')
    print(f'  Hasil: {PASS} OK | {WARN} peringatan | {FAIL} gagal')
    print('========================================')
    if FAIL:
        sys.exit(1)


if __name__ == '__main__':
    main()
