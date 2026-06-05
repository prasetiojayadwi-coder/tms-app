"""Cek & inisialisasi Supabase TMS secara otomatis."""
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def load_config():
    for name in ('config.js', 'config.deploy.js'):
        p = ROOT / name
        if not p.exists():
            continue
        text = p.read_text(encoding='utf-8')
        url_m = re.search(r"url:\s*['\"]([^'\"]+)['\"]", text)
        key_m = re.search(r"anonKey:\s*['\"]([^'\"]+)['\"]", text)
        if url_m and key_m:
            return url_m.group(1).strip(), key_m.group(1).strip()
    raise SystemExit('config.js / config.deploy.js tidak ditemukan')

def api(url, key, path, method='GET', body=None):
    req = urllib.request.Request(
        f'{url.rstrip("/")}{path}',
        data=json.dumps(body).encode() if body is not None else None,
        method=method,
        headers={
            'apikey': key,
            'Authorization': f'Bearer {key}',
            'Content-Type': 'application/json',
            'Prefer': 'return=minimal',
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')

def main():
    print('=== TMS Supabase Setup Otomatis ===\n')
    base, key = load_config()
    print(f'Project: {base}\n')

    status, body = api(base, key, '/rest/v1/tms_sync?select=id,db_version&limit=1')
    print(f'[1] Cek tabel tms_sync ... HTTP {status}')

    if status == 404 or 'PGRST205' in body or 'does not exist' in body.lower():
        print('\n[PERLU] Tabel belum ada. SQL harus dijalankan di Supabase Dashboard.')
        print('        Buka: https://supabase.com/dashboard/project/mezuatmcjqjxfsvepizv/sql/new')
        print('        File: supabase_setup.sql (copy-paste > Run)')
        raise SystemExit(2)

    if status not in (200, 206):
        print('Body:', body[:300])
        print('\n[GAGAL] Akses tabel bermasalah. Pastikan supabase_setup.sql sudah di-Run.')
        raise SystemExit(1)

    rows = json.loads(body) if body.strip() else []
    print(f'    Tabel OK. Baris data: {len(rows)}')

    if not rows:
        print('\n[2] Inisialisasi baris awal tms_sync ...')
        payload = {
            'id': 1,
            'db_version': 1,
            'db_data': {
                'version': 1,
                'users': {},
                'tools': [],
                'demoUnits': [],
                'requests': [],
                'historyLog': [{'id': 1, 'time': '2026-01-01T00:00:00.000Z', 'action': 'Cloud database diinisialisasi.'}],
                'messages': [],
                'serviceTickets': [],
                'deletedIds': [],
            },
        }
        st, res = api(base, key, '/rest/v1/tms_sync', 'POST', payload)
        print(f'    HTTP {st}')
        if st not in (200, 201, 204):
            print('    Gagal insert:', res[:300])
            raise SystemExit(1)
        print('    Baris awal berhasil dibuat.')
    else:
        print('\n[2] Data cloud sudah ada — lewati inisialisasi.')

    print('\n[3] Cek aplikasi online ...')
    try:
        with urllib.request.urlopen('https://prasetiojayadwi-coder.github.io/tms-app/config.deploy.js', timeout=15) as r:
            ok = r.status == 200
    except Exception:
        ok = False
    print(f'    config.deploy.js online: {"OK" if ok else "CEK MANUAL"}')

    print('\n=== SELESAI ===')
    print('URL untuk tim: https://prasetiojayadwi-coder.github.io/tms-app/')
    print('Login: admin / admin')
    print('Badge "Cloud Live" (hijau) = realtime aktif.')

if __name__ == '__main__':
    main()
