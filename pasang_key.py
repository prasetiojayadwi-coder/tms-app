"""Pasang Supabase key ke config.js + config.deploy.js, cek koneksi, push GitHub."""
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
URL = 'https://mezuatmcjqjxfsvepizv.supabase.co'
GIT = r'C:\Program Files\Git\cmd\git.exe'


def read_key():
    key_file = ROOT / 'supabase.key'
    if key_file.exists():
        key = key_file.read_text(encoding='utf-8').strip().strip("'\"")
        if key:
            print(f'[INFO] Key dibaca dari {key_file.name}')
            return key
    if len(sys.argv) > 1:
        return sys.argv[1].strip().strip("'\"")
    print('Paste Publishable Key (api_tms / sb_publishable_...) lalu Enter:')
    return input('> ').strip().strip("'\"")


def validate_key(key):
    if not key:
        raise SystemExit('[ERROR] Key kosong.')
    if key.startswith('sb_secret_'):
        raise SystemExit('[ERROR] Ini Secret Key — gunakan Publishable Key (sb_publishable_...).')
    if not (key.startswith('eyJ') or key.startswith('sb_publishable_')):
        raise SystemExit('[ERROR] Format key tidak dikenali. Copy dari baris api_tms di Supabase.')


def write_configs(key):
    local = f"""/**
 * TMS Cloud Configuration — dibuat otomatis oleh Pasang_Cloud.bat
 */
window.TMS_CONFIG = {{
    supabase: {{
        url: '{URL}',
        anonKey: '{key}'
    }}
}};
"""
    deploy = f"""/**
 * TMS Cloud — konfigurasi deploy online (GitHub Pages).
 */
window.TMS_CONFIG = {{
    supabase: {{
        url: '{URL}',
        anonKey: '{key}'
    }}
}};
"""
    (ROOT / 'config.js').write_text(local, encoding='utf-8')
    (ROOT / 'config.deploy.js').write_text(deploy, encoding='utf-8')
    print('[OK] config.js + config.deploy.js disimpan.')


def test_cloud(key):
    req = urllib.request.Request(
        f'{URL}/rest/v1/tms_sync?select=id&limit=1',
        headers={
            'apikey': key,
            'Authorization': f'Bearer {key}',
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            if r.status not in (200, 206):
                raise SystemExit(f'[GAGAL] HTTP {r.status} — key tidak bisa akses tms_sync.')
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8', 'replace')
        raise SystemExit(f'[GAGAL] HTTP {e.code} — {body[:200]}')
    print('[OK] Koneksi Supabase tms_sync berhasil.')


def git_push():
    if not Path(GIT).exists():
        print('[WARN] Git tidak ditemukan — lewati push. Push manual config.deploy.js nanti.')
        return
    subprocess.run([GIT, 'add', 'config.deploy.js'], cwd=ROOT, check=True)
    diff = subprocess.run([GIT, 'diff', '--cached', '--quiet'], cwd=ROOT)
    if diff.returncode == 0:
        print('[INFO] config.deploy.js tidak berubah — lewati commit.')
        return
    subprocess.run(
        [GIT, 'commit', '-m', 'Update Supabase publishable key untuk cloud sync online.'],
        cwd=ROOT, check=True,
    )
    push = subprocess.run([GIT, 'push', 'origin', 'main'], cwd=ROOT)
    if push.returncode == 0:
        print('[OK] Push GitHub berhasil — deploy otomatis dalam 1-2 menit.')
    else:
        print('[WARN] Push gagal — jalankan manual: git push origin main')


def main():
    print('=== TMS — Pasang Cloud Key ===\n')
    key = read_key()
    validate_key(key)
    write_configs(key)
    test_cloud(key)
    git_push()
    print('\n=== SELESAI ===')
    print('Lokal : Mulai_Server.bat → badge Cloud Live hijau')
    print('Online: https://prasetiojayadwi-coder.github.io/tms-app/')
    print('        (tunggu 1-2 menit setelah push)')


if __name__ == '__main__':
    main()
